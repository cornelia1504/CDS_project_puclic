# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on mai 2023

@author: Mamitiana Mahitasoa

"""
import re
import os
import time
import json
import zlib
from xml.etree import ElementTree
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.adapters import HTTPAdapter, Retry
import retrieve_db_info as db
import pandas as pd
import alphafold as alf

POLLING_INTERVAL = 3
API_URL = "https://rest.uniprot.org"


retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))


def check_response(response):
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print(response.json())
        raise


def submit_id_mapping(from_db, to_db, ids):
    request = requests.post(
        f"{API_URL}/idmapping/run",
        data={"from": from_db, "to": to_db, "ids": ",".join(ids)},
    )
    check_response(request)
    return request.json()["jobId"]


def get_next_link(headers):
    re_next_link = re.compile(r'<(.+)>; rel="next"')
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)


def check_id_mapping_results_ready(job_id):
    while True:
        request = session.get(f"{API_URL}/idmapping/status/{job_id}")
        check_response(request)
        j = request.json()
        if "jobStatus" in j:
            if j["jobStatus"] == "RUNNING":
                print(f"Retrying in {POLLING_INTERVAL}s")
                time.sleep(POLLING_INTERVAL)
            else:
                raise Exception(j["jobStatus"])
        else:
            return bool(j["results"] or j["failedIds"])


def get_batch(batch_response, file_format, compressed):
    batch_url = get_next_link(batch_response.headers)
    while batch_url:
        batch_response = session.get(batch_url)
        batch_response.raise_for_status()
        yield decode_results(batch_response, file_format, compressed)
        batch_url = get_next_link(batch_response.headers)


def combine_batches(all_results, batch_results, file_format):
    if file_format == "json":
        for key in ("results", "failedIds"):
            if key in batch_results and batch_results[key]:
                all_results[key] += batch_results[key]
    elif file_format == "tsv":
        return all_results + batch_results[1:]
    else:
        return all_results + batch_results
    return all_results


def get_id_mapping_results_link(job_id):
    url = f"{API_URL}/idmapping/details/{job_id}"
    request = session.get(url)
    check_response(request)
    #print('****', request.json())
    return request.json()["redirectURL"]


def decode_results(response, file_format, compressed):
    if compressed:
        decompressed = zlib.decompress(response.content, 16 + zlib.MAX_WBITS)
        if file_format == "json":
            j = json.loads(decompressed.decode("utf-8"))
            return j
        elif file_format == "tsv":
            return [line for line in decompressed.decode("utf-8").split("\n") if line]
        elif file_format == "xlsx":
            return [decompressed]
        elif file_format == "xml":
            return [decompressed.decode("utf-8")]
        else:
            return decompressed.decode("utf-8")
    elif file_format == "json":
        return response.json()
    elif file_format == "tsv":
        return [line for line in response.text.split("\n") if line]
    elif file_format == "xlsx":
        return [response.content]
    elif file_format == "xml":
        return [response.text]
    return response.text


def get_xml_namespace(element):
    m = re.match(r"\{(.*)\}", element.tag)
    return m.groups()[0] if m else ""


def merge_xml_results(xml_results):
    merged_root = ElementTree.fromstring(xml_results[0])
    for result in xml_results[1:]:
        root = ElementTree.fromstring(result)
        for child in root.findall("{http://uniprot.org/uniprot}entry"):
            merged_root.insert(-1, child)
    ElementTree.register_namespace("", get_xml_namespace(merged_root[0]))
    return ElementTree.tostring(merged_root, encoding="utf-8", xml_declaration=True)


def print_progress_batches(batch_index, size, total):
    n_fetched = min((batch_index + 1) * size, total)
    print(f"Fetched: {n_fetched} / {total}")


def get_id_mapping_results_search(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    file_format = query["format"][0] if "format" in query else "json"
    if "size" in query:
        size = int(query["size"][0])
    else:
        size = 500
        query["size"] = size
    compressed = (
        query["compressed"][0].lower() == "true" if "compressed" in query else False
    )
    parsed = parsed._replace(query=urlencode(query, doseq=True))
    url = parsed.geturl()
    request = session.get(url)
    check_response(request)
    results = decode_results(request, file_format, compressed)
    #
    m= request.headers
    print(m)
    #
    total = int(request.headers["x-total-results"])
    print_progress_batches(0, size, total)
    for i, batch in enumerate(get_batch(request, file_format, compressed), 1):
        results = combine_batches(results, batch, file_format)
        print_progress_batches(i, size, total)
    if file_format == "xml": #xml
        return merge_xml_results(results)
    return results


def get_id_mapping_results_stream(url):
    if "/stream/" not in url:
        url = url.replace("/results/", "/results/stream/")
    request = session.get(url)
    check_response(request)
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    file_format = query["format"][0] if "format" in query else "json"
    compressed = (
        query["compressed"][0].lower() == "true" if "compressed" in query else False
    )
    return decode_results(request, file_format, compressed)


#######################################################################################
def id_mapping_cazy_uniprot(family):
    """mapping des accessions cazy contre uniprotKB """
    print('*********Id_mapping UniprotKB************')
    accession_numbers = db.accession_ncbi_join(family)

    job_id = submit_id_mapping(
        from_db="EMBL-GenBank-DDBJ_CDS", to_db="UniProtKB", ids=accession_numbers)
    if check_id_mapping_results_ready(job_id):
        link = get_id_mapping_results_link(job_id)
        print(link)
        results = get_id_mapping_results_search(link)
    ligne = results.__str__()

    # Extraction des informations souhaitées avec la méthode re.findall()
    from_value = re.findall(r"'from': '([^']+)'", ligne)
    primaryAccession = re.findall(r"'primaryAccession': '([^']+)'", ligne)
    failedIds = re.findall(r"'failedIds': (\[[^\]]+\])", ligne)
    #failedIds = re.findall(r"'failedIds': '([^']+)'", failedIds.__str__())

    # Création des dictionnaires avec les informations extraites
    dico1 = {'from': from_value[0]} if from_value else {}
    dico2 = {'primaryAccession': primaryAccession[0]} if primaryAccession else {}
    dico3 = {'failedIds': failedIds[0]} if failedIds else {}

    #gestion des listes en dico
    cazy_accessions = from_value
    uniprot_accesions = primaryAccession
    dico_accessions = dict(zip(uniprot_accesions, cazy_accessions))

    # Affichage des dictionnaires créés

    # Création d'un dictionnaire avec les valeurs extraites pour ce groupe
    group_dict = {'from': from_value, 'accession_uniprot': primaryAccession, 'failedIds': failedIds}
    groups = []  # Liste pour stocker les groupes d'informations
    # Ajout du dictionnaire à la liste des groupes
    groups.append(group_dict)
    #print('\n', groups)
    return uniprot_accesions, cazy_accessions, dico_accessions

#######################################################################################
def clustering_uniprot_uniref50(family):
    """mapping des accessions cazy contre uniprotKB """
    print('*********Id_mapping Uniref50************')

    accession_numbers = id_mapping_cazy_uniprot(family)
    accession_numbers = accession_numbers[0]

    job_id = submit_id_mapping(
        from_db="UniProtKB_AC-ID", to_db="UniRef50", ids=accession_numbers)
    if check_id_mapping_results_ready(job_id):
        link = get_id_mapping_results_link(job_id)
        print(link)
        results = get_id_mapping_results_search(link)

    ligne = results.__str__()
    # Extraction des informations souhaitées avec la méthode re.findall()
    id_value = re.findall(r"'id': '([^']+)'", ligne)
    from_value = re.findall(r"'from': '([^']+)'", ligne)
    members_value = re.findall(r"'members': (\[[^\]]+\])", ligne)
    failedIds = re.findall(r"'failedIds': (\[[^\]]+\])", ligne)

    # gestion des listes en dico
    uniprot_accesions = from_value
    uniref50_cluster = id_value
    dico_cluster50 = dict(zip(uniprot_accesions,uniref50_cluster))

    # Affichage des dictionnaires créés
    df = pd.DataFrame({'cluster50': list(dico_cluster50.values()), 'accession': list(dico_cluster50.keys())})
    grouped = df.groupby('cluster50')['accession'].apply(list)
    new_df = grouped.reset_index()

    return grouped, new_df, dico_cluster50

#alfafold
def search_accession_alf_50(family):
    results = clustering_uniprot_uniref50(family)
    uniprot_accesions = results[0]
    uniref50_cluster = results[1]
    new_df = results[1]

    #ids_for_alph():
    code_alf = []
    code_alf_dwl = []
    cluster_files_list = []
    for key in new_df['cluster50']:
        accession = key.split('_')[1]
        if len(accession) == 6:
            #print(accession, 'valable')
            code_alf.append(accession)
            continue
        if len(accession) != 6:
            #print(accession, 'non valable')
            code_alf_dwl.append(accession)
            cluster = key
            # file = f'{key}_cluster50.list'
            # print(file)
            file = f'{accession}_cluster50.list'
            #print(file)
            directory = f'/home/guest/Documents/Cornelia/cds_project/{family}/list_accession_clt50'
            if not os.path.exists(directory):
                os.mkdir(directory)
            file = f'/home/guest/Documents/Cornelia/cds_project/{family}/list_accession_clt50/{file}'
            os.system(f'wget -q -O {file} https://rest.uniprot.org/uniref/{cluster}/members?format=list&size=500 > {file}')
            if os.path.isfile(file):
                #print(f"Le fichier {file} a été téléchargé avec succès.")
                cluster_files_list.append(file)
            else:
                print(f"Une erreur est survenue lors du téléchargement de {file}.")

    print('Nomnbre d`accessions avec un modèle alphaFold disponible : ',len(code_alf))
    print('Nomnbre d`accessions avec un modèle alphaFold non disponible : ',len(code_alf_dwl))
    #print(cluster_files_list)
    #download pdb filees
    print('\n ***************** download ******************* \n')
    output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/modeles_alph_clt'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for accession in code_alf:
        output_file = os.path.join(output_folder, f"{accession}_al.pdb")
        os.system(f'wget -O {output_file} https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v4.pdb')
        #https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-model_v4.pdb

    return cluster_files_list, code_alf, code_alf_dwl
#15 mai
def retrieve_alf(family):
    all_accession_alf = []
    no_alf_acs = []
    directory = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/list_accession_clt50'#

    if not os.path.exists(directory):
        os.mkdir(directory)
    file_names = os.listdir(f'{directory}')
    dico_accession_alf = {}
    for name in file_names:
        file = f'{directory}/{name}'
        print('file : ', file)
        with open(f'{file}', 'r') as f:
            accession_alf_list = []
            for line in f.readlines():
                print('****line**** ', line)
                print('ligne : ', line)
                pattern = r"\b\w{6}(?=_)"
                regex = re.compile(pattern)
                result = regex.findall(line)
                print(result)
                if result:
                    dico_accession_alf[name[0:9]] = result[0]
                    accession_alf_list.append(result[0])
                    break  # sortir de la boucle dès qu'on trouve l'accession à 6 caractères
            if accession_alf_list:
                premier_element = accession_alf_list[0]
            else:
                print("Aucune accession ayant un modèle a été trouvé dans cette liste !")
                premier_element = None
                no_alf_acs.append(name[0:10])
            if premier_element != None:
                all_accession_alf.append(premier_element)
    print('dico : ', dico_accession_alf)
    print('liste finale : ',all_accession_alf)
    print('********', len(all_accession_alf))
    print('\n ******************** \n')
    print('********', len(no_alf_acs))

    return dico_accession_alf, all_accession_alf
def download_models(family):
    """function to retrieve alphafold modeles pdb files of a list of accession"""
    global output_folder
    output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/modeles_alf_clt'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # accession_search = retrieve_alf(family)
    # dico_accessions = accession_search[0]
    search_accession = search_accession_alf_50(family)
    code_alf = search_accession[1]
    code_alf_dwl = search_accession[2]
    print('**************************** \n')
    retieve = alf.retrieve_alf(family)
    all_accession_alf = retieve[1]
    dwl_accessions = code_alf.__str__() + all_accession_alf.__str__()
    print('\n **** code_alf accessions : ', code_alf)
    print(len(code_alf))
    print('\n **** all accessions : ', all_accession_alf)
    print(len(all_accession_alf))
    print('\n **** dwl accessions : ', dwl_accessions)
    print(len(dwl_accessions))

def map_acc_org(family):
    result = db.organisme(family)
    dico_org = result[0]
    results = clustering_uniprot_uniref50(family)
    uniprot_accesions = results[0]
    uniref50_cluster = results[1]
    new_df = results[1]
    print(new_df)

#######################################################################################
def id_mapping_uniprot_uniref50(family):
    """mapping des accessions cazy contre uniprotKB """
    print('*********Id_mapping Uniref50************')

    accession_numbers = id_mapping_cazy_uniprot(family)
    accession_numbers = accession_numbers[0]

    job_id = submit_id_mapping(
        from_db="UniProtKB_AC-ID", to_db="UniRef50", ids=accession_numbers)
    if check_id_mapping_results_ready(job_id):
        link = get_id_mapping_results_link(job_id)
        print(link)
        results = get_id_mapping_results_search(link)
    #print('Analyse : ',results)
    ligne = results.__str__()

    # Extraction des informations souhaitées avec la méthode re.findall()
    id_value = re.findall(r"'id': '([^']+)'", ligne)
    from_value = re.findall(r"'from': '([^']+)'", ligne)
    members_value = re.findall(r"'members': (\[[^\]]+\])", ligne)
    failedIds = re.findall(r"'failedIds': (\[[^\]]+\])", ligne)

    # Création des dictionnaires avec les informations extraites
    dico1 = {'cluster_50': id_value[0]} if id_value else {}
    dico2 = {'from': from_value[0]} if from_value else {}
    dico3 = {'members': members_value[0]} if members_value else {}
    dico4 = {'failedIds': failedIds[0]} if failedIds else {}

    # gestion des listes en dico
    uniprot_accesions = from_value
    uniref50_cluster = id_value
    dico_cluster50 = dict(zip(uniprot_accesions,uniref50_cluster))

    # Affichage des dictionnaires créés
    # print(dico1)
    print(uniref50_cluster)
    print(uniprot_accesions)
    print(dico_cluster50)
    # Création d'un dictionnaire avec les valeurs extraites pour ce groupe
    group_dict = {'uniprot_accesions': from_value, 'uniref50_cluster': id_value, 'failedIds': failedIds}
    groups = []  # Liste pour stocker les groupes d'informations
    # Ajout du dictionnaire à la liste des groupes
    groups.append(group_dict)
    print('\n', groups)
    return uniprot_accesions, uniref50_cluster, dico_cluster50

#######################################################################################
#https://rest.uniprot.org/uniref/UniRef50_P96463/members?format=list&size=500
#https://rest.uniprot.org/uniref/UniRef50_P96463/members?format=list&size=500
###########################################################
def search_accession_alf(family):
    results = id_mapping_uniprot_uniref50(family)
    uniprot_accesions = results[0]
    uniref50_cluster = results[1]
    dico_accessions = results[2]
    print(dico_accessions)
    #ids_for_alph():
    code_alf = []
    code_alf_dwl = []
    cluster_files_list = []
    for key in dico_accessions.keys():
        if len(key.strip()) == 6:
            print(key, 'valable')
            code_alf.append(key)
            continue
        if len(key.strip()) != 6:
            print(key, 'non valable')
            code_alf_dwl.append(key)
            cluster = dico_accessions[key]
            # file = f'{key}_cluster50.list'
            # print(file)
            file = f'{key}_cluster50.list'
            #print(file)
            file = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/list_accession_clt50/{file}'
            print('*************************')
            os.system(f'wget -q -O {file} https://rest.uniprot.org/uniref/{cluster}/members?format=list&size=500 > {file}')
            if os.path.isfile(file):
                print(f"Le fichier {file} a été téléchargé avec succès.")
                cluster_files_list.append(file)
            else:
                print(f"Une erreur est survenue lors du téléchargement de {file}.")
    print('Nomnbre d`accessions avec un modèle alphaFold disponible : ',len(code_alf))
    print('Nomnbre d`accessions avec un modèle alphaFold non disponible : ',len(code_alf_dwl))
    print(cluster_files_list)
    return cluster_files_list

def for_alf(family):
    test = search_accession_alf(family)
    return test
#######################################################################################

def parser():
    with open('cluster_name_test_json.json', 'r') as f:
        ligne = f.read()

        # Extraction des informations souhaitées avec la méthode re.findall()
        id_value = re.findall(r"'id': '([^']+)'", ligne)
        from_value = re.findall(r"'from': '([^']+)'", ligne)
        members_value = re.findall(r"'members': (\[[^\]]+\])", ligne)

        # Création des dictionnaires avec les informations extraites
        dico1 = {'cluster_50': id_value[0]} if id_value else {}
        dico2 = {'from': from_value[0]} if from_value else {}
        dico3 = {'members': members_value[0]} if members_value else {}

        # Affichage des dictionnaires créés
        print(dico1)
        print(dico2)
        print(dico3)

        # Création d'un dictionnaire avec les valeurs extraites pour ce groupe
        group_dict = {'id': id_value, 'from': from_value, 'members': members_value}
        groups = []  # Liste pour stocker les groupes d'informations
        # Ajout du dictionnaire à la liste des groupes
        groups.append(group_dict)
        print('\n', groups)

if __name__ == '__main__':
    family = input('family g : ')
    #id_mapping_uniprot_uniref50(family)
    #clustering_uniprot_uniref50(family)
    search_accession_alf_50(family) #
    #retrieve_alf(family)
    #download_models(family)
    #search_accession_alf(family)
    #map_acc_org(family)
    print('\n **********************')
    #for_alf(family)