import os
import requests
from bs4 import BeautifulSoup
import urllib.request

# Fonction pour récupérer les fichiers PDB pour une famille donnée
def get_pdbs_for_family(family_name):
    # URL de recherche sur RCSB PDB pour la famille donnée
    search_url = 'https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_polymer_entity_annotation.annotation_family_name%22%2C%22operator%22%3A%22exact_match%22%2C%22value%22%3A%22' + family_name + '%22%7D%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22pager%22%3A%7B%22start%22%3A0%2C%22rows%22%3A1000%7D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%2C%22query_info%22%3A%7B%22ignored_words%22%3A%5B%5D%7D%7D%7D'

    # Envoi de la requête HTTP
    response = requests.get(search_url)

    # Analyse de la réponse HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Recherche des identifiants PDB dans le HTML
    pdb_ids = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/structure/'):
            pdb_id = href.split('/')[-1]
            pdb_ids.append(pdb_id)

    # Téléchargement des fichiers PDB
    for pdb_id in pdb_ids:
        pdb_url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
        pdb_file = f'{pdb_id}.pdb'
        urllib.request.urlretrieve(pdb_url, pdb_file)

    print(f'Downloaded {len(pdb_ids)} PDB files for family {family_name}')

# Exemple d'utilisation
family_name = input('Enter family name: ')
get_pdbs_for_family(family_name)