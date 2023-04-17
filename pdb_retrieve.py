import requests
from bs4 import BeautifulSoup
import urllib.request

# Paramètres de recherche

search_term = input('Enter family name: ')
search_for = "Sequence"

# URL de la recherche avancée
url = 'https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22full_text%22%2C%22parameters%22%3A%7B%22value%22%3A%22' + search_term + '%22%7D%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22full_text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%2C%22scoring_strategy%22%3A%22combined%22%7D%2C%22request_info%22%3A%7B%22query_id%22%3A%2208bdfe56bf19bac7aa209b3f28b448c7%22%7D%7D'
url = "https://www.rcsb.org/pdb/search/advSearch.do"

# Paramètres de la requête POST
data = {
    "f": search_for,
    "q": search_term,
    "nStructsPerPage": 250,
    "start": 0,
    "currentTab": "structuresTab",
    "pdbIds": "",
    "experimentalMethod": "",
    "resolutionHigh": "",
    "resolutionLow": "",
    "sequenceLengthMax": "",
    "sequenceLengthMin": "",
    "pwSummaryThreshold": "",
    "pwSummaryMethod": "all",
    "orgDetails": "",
    "includeObsolete": "true",
    "sortField": "score desc, releaseDate desc",
    "qrid": "",
    "exactMatch": "off",
    "refineQuery": "true",
    "externalId": "",
    "ntgt": "",
    "polymer": "1",
    "nonpolymer": "1",
    "ligand": "1",
    "dna": "0",
    "rna": "0",
    "complexity": "",
    "targetedStructuresTabGuid": "",
    "nTargetsPerPage": "10",
    "currentTabTargets": "targetsTab",
    "tab": "",
    "clusterExpand": "",
    "accessionId": "",
    "targetKey": "",
    "subtarg": "",
    "node": "",
    "allergen": "",
    "taxDetails": "",
    "taxId": "",
    "showingResultsFor": search_term,
    "resultTypes": "",
    "inputTab": "searchTab",
    "hideAdvSearchForm": "",
    "keywords": "",
    "cluster": "",
    "csrftoken": "",
}

# Envoi de la requête POST pour obtenir les résultats de recherche
response = requests.post(url, data=data)

# Analyse de la page HTML des résultats de recherche à l'aide de BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")
pdb_ids = []

# Boucle pour récupérer les identifiants PDB des structures correspondant à la recherche
for row in soup.find_all("tr", {"class": "pdbresultrow"}):
    pdb_id = row.find_all("td")[0].text.strip()
    pdb_ids.append(pdb_id)

# Boucle pour télécharger les fichiers PDB des structures
for pdb_id in pdb_ids:
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    urllib.request.urlretrieve(url, f"{pdb_id}.pdb")

output_directory = input("chemin vers repertoire de sortie:")
with open(output_directory + "result.txt", "w") as output_file:
    output_file.write("Voici le résultat de mon programme!")