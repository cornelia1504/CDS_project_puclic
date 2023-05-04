import re
import os
import time
import json
import zlib
from xml.etree import ElementTree
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.adapters import HTTPAdapter, Retry
import csv
import pandas as pd

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
    #https://rest.uniprot.org/idmapping/uniprotkb/results/stream/{job_id}?compressed=true&fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength%2Ccc_developmental_stage%2Ccc_induction%2Cft_chain%2Cxref_ccds%2Cxref_embl&format=tsv
    #url = f"{API_URL}/idmapping/uniprotkb/results/stream/{job_id}?compressed=true&fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength%2Ccc_developmental_stage%2Ccc_induction%2Cft_chain%2Cxref_ccds%2Cxref_embl&format=list"
    request = session.get(url)
    check_response(request)
    print('****', request.json())
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
    #total = int(request.headers["X-UniProt-Release"])###

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

with open('accession_numbers.txt') as f:
    accession_numbers = f.read().strip().split('\n')
    print(accession_numbers)
    accession_numbers=  accession_numbers[1:3]
    for i in accession_numbers :
        id = i
    ids = ",".join(accession_numbers)
    print(ids)
    job_id = submit_id_mapping(
        from_db="UniProtKB_AC-ID", to_db="UniRef50", ids=[ids, "P12345"]
    )
    if check_id_mapping_results_ready(job_id):
        link = get_id_mapping_results_link(job_id)
        print(link)
        #link = f'{API_URL}/idmapping/uniprotkb/results/stream/{job_id}?compressed=true&fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength%2Ccc_developmental_stage%2Ccc_induction%2Cft_chain%2Cxref_ccds%2Cxref_embl&format=list'

        results = get_id_mapping_results_search(link)
        # Equivalently using the stream endpoint which is more demanding
        # on the API and so is less stable:
        # results = get_id_mapping_results_stream(link)
        ##results = get_id_mapping_results_stream(f"https://rest.uniprot.org/idmapping/uniprotkb/results/stream/{job_id}?compressed=true&fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength%2Ccc_developmental_stage%2Ccc_induction%2Cft_chain%2Cxref_ccds%2Cxref_embl&format=tsv")
        ##results = get_id_mapping_results_search(f"https://rest.uniprot.org/idmapping/uniprotkb/results/stream/{job_id}?download=true&format=list")
        #https://rest.uniprot.org/idmapping/uniprotkb/results/stream/{job_id}?download=true&format=list
print(results)

with open('cluster_name_test.json', 'w') as f:
    print(results, file=f)
#####################
with open('cluster_name_test.json', 'r') as f:
    data = f.readlines()
    data_json = json.dumps(data)
    print(data)
    print(data_json)
with open('cluster_name_test_json.json', 'w') as f:
    print(data_json, file=f)
with open('cluster_name_test_json.json') as json_file:
    jsondata = json.load(json_file)
    print(jsondata)
# #     print("Nom:", jsondata['from'][0])
# #     print("Âge:", jsondata['id'][0])
# #     print("Ville:", jsondata['name'][0])
# # data_file = open('cluster_name_test_json.csv', 'w', newline='')
# csv_writer = csv.writer(data_file)
####################################################################
import subprocess

# Chemin du fichier JSON à reformater
json_file_path = "cluster_name_test_json.json"

# Commande jq pour reformater le fichier avec des indentations
command = ["jq", ".", json_file_path]

# Exécution de la commande jq en utilisant la bibliothèque subprocess
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Vérification si la commande a échoué
if result.returncode != 0:
    print("La commande a échoué :", result.stderr)
else:
    # Récupération du fichier JSON reformatté
    reformatted_json = result.stdout

    # Affichage du fichier JSON reformatté
    print(reformatted_json)

# Chemin du nouveau fichier JSON
new_json_file_path = "fichier_formate_test.json"

# Ouverture du nouveau fichier en mode écriture
with open(new_json_file_path, "w") as f:
    # Écriture du fichier JSON reformatté dans le nouveau fichier
    f.write(reformatted_json)
##############################################################

# Charger le fichier JSON reformatté
with open('fichier_formate_test.json', 'r') as f:
    data = json.load(f)

# Créer un DataFrame pandas à partir du fichier JSON
df = pd.json_normalize(data)
print('*************')
print(df.columns)
# Sélectionner les colonnes que vous souhaitez inclure dans le fichier CSV
selected_cols = ['id', 'from', 'name']

# Écrire le DataFrame pandas dans un fichier CSV
df[selected_cols].to_csv('nouveau_fichier.csv', index=False)
##############################################################

# df = pd.read_json (r'cluster_name_test_json.json')
# df.to_csv (r'cluster_name_test_json.csv', index= None)
# print(df)
# df = pd.read_json (r'cluster_name_test.json')
# df.to_csv (r'cluster_name_test.txt.csv')
#####################



def get_data_frame_from_tsv_results(tsv_results):
    reader = csv.DictReader(tsv_results, delimiter="\t", quotechar='"')
    return pd.DataFrame(list(reader))
seuil = 50
output_folder = f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster{seuil}_name'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_file = "cluster_test.tsv"
tsv = get_id_mapping_results_stream(f"https://rest.uniprot.org/idmapping/uniprotkb/results/stream/{job_id}?compressed=true&fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength%2Ccc_developmental_stage%2Ccc_induction%2Cft_chain%2Cxref_ccds%2Cxref_embl&format=tsv")
with open('cluster_test.tsv', 'w') as f:
    print(tsv, file=f)