"""Ce script contient les fonctions necessaires à la gestion des tableaux"""
import pandas as pd
import io
import re
import time
import json
import zlib
from xml.etree import ElementTree
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.adapters import HTTPAdapter, Retry
import retrieve_db_info as db


POLLING_INTERVAL = 3
API_URL = "https://rest.uniprot.org"


retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))

#################################################################
def accession_nb_uniref50():
    """mapping d' accession_numbers.txt contre uniref50 """
    url = 'https://rest.uniprot.org/uniprotkb/accessions'
    #url = 'https://rest.uniprot.org/idmapping/run'
    # url = 'https://www.uniprot.org/uploadlists/'
    with open('accession_numbers.txt') as f:
        accession_numbers = f.read().strip().split('\n')
        accession_numbers=  accession_numbers[1:3]
    params = {
        'from': 'UniProtKB_AC-ID',
        'to': 'UniRef50',
        # 'format': 'tab',
        'accessions': ','.join(accession_numbers)
    }

    response = requests.get(url, params=params)

    # Utilisation de io.StringIO pour créer un objet file-like à partir des données de réponse
    file_like_object = io.StringIO(response.content.decode())
    print(file_like_object)
    # Utilisation de l'objet file-like avec pd.read_csv
    df = pd.read_csv(file_like_object, sep='\t')
    print(df)
    df.to_excel('accession_numbers_uniref50.xlsx', index=False)
###################################################"

def check_response(response):
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print(response.json())
        raise
def id_mapp_50():
    """mapping d' accession_numbers.txt contre uniref50 """
    with open('accession_numbers.txt') as f:
        accession_numbers = f.read().strip().split('\n')
        accession_numbers=  accession_numbers[1:3]
    request = requests.post(
        f"{API_URL}/idmapping/run",
        data={"from": 'UniProtKB_AC-ID', "to": 'UniRef50', "ids": ",".join(accession_numbers)},
    )
    check_response(request)
    r =request.json()["jobId"]
    print(r)
    return request.json()["jobId"]

#####################################################################
def id_mapping_uniref50():
    """mapping d' accession_numbers.txt contre uniref50 """
    pass

#####################################################################
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
    total = int(request.headers["x-total-results"])
    print_progress_batches(0, size, total)
    for i, batch in enumerate(get_batch(request, file_format, compressed), 1):
        results = combine_batches(results, batch, file_format)
        print_progress_batches(i, size, total)
    if file_format == "xml":
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


# job_id = submit_id_mapping(
#     from_db="UniProtKB_AC-ID", to_db="ChEMBL", ids=["P05067", "P12345"]
# )
# if check_id_mapping_results_ready(job_id):
#     link = get_id_mapping_results_link(job_id)
#     results = get_id_mapping_results_search(link)
#     # Equivalently using the stream endpoint which is more demanding
#     # on the API and so is less stable:
#     # results = get_id_mapping_results_stream(link)
#
# print(results)
########################################################
def id_mapping_uniprotKB(family):
    """mapping des accessions cazy contre uniprotKB """
    accession_numbers = db.accession_ncbi_join(family)
    accession_numbers = accession_numbers[1:5]
    request = requests.post(
        f"{API_URL}/idmapping/run",
        data={"from": 'EMBL-GenBank-DDBJ_CDS', "to": 'UniProtKB', "ids": ",".join(accession_numbers)},
    )
    check_response(request)
    r = request.json()["jobId"]
    print(r)
    print('*****accessions cazy******* : ', accession_numbers)
    return request.json()["jobId"]

#
# if check_id_mapping_results_ready(job_id):
#     link = get_id_mapping_results_link(job_id)
#     results = get_id_mapping_results_search(link)


#########################################################
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

def parser2():
    with open('cluster_name_test_json.json', 'r') as f:
        ligne = f.read() #.strip()

    # Motif de recherche pour extraire les informations de chaque groupe
    pattern = r"'id': '([^']+)'[^}]+?'from': '([^']+)'[^}]+?'members': (\[[^\]]+\])"

    # Recherche de tous les groupes d'informations dans la ligne
    matches = re.finditer(pattern, ligne)

    # Stockage de chaque groupe d'informations dans un dictionnaire
    result = []
    for match in matches:
        id_value = match.group(1)
        from_value = match.group(2)
        members_value = match.group(3)

        group = {'id': id_value, 'from': from_value, 'members': members_value}
        result.append(group)

    print(result)


if __name__ == '__main__':
    family = input('family : ')
    job_id = id_mapping_uniprotKB(family)
    print(job_id)
    statut = check_id_mapping_results_ready(job_id)
    print(statut)
    url = get_id_mapping_results_link(job_id)
    print(url)
    parser()
    print('*****************************************')
    parser2()