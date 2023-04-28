""""""
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Récupération de la page web contenant le tableau
url = 'http://www.cazy.org/GH62_structure.html'
response = requests.get(url)

# Extraction du tableau avec BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')

# Conversion du tableau HTML en dataframe Pandas
df = pd.read_html(str(table))[0]

# Sauvegarde du dataframe dans un fichier Excel
df.to_excel('tableau_cazy.xlsx', index=False)

############################################################################
import pandas as pd

url = 'http://www.cazy.org/GH62_structure.html'

tables = pd.read_html(url)
df = tables[1]

# Supprimer la dernière ligne qui contient des informations inutiles
df = df.iloc[:-1]

# # Renommer les colonnes
# df.columns = ['Protein Name', 'EC', 'Organism', 'GenBank', 'Uniprot', 'PDB/3D', 'Carbohydrate Ligands', 'Resolution (Å)']

# Enregistrer le dataframe dans un fichier CSV
df.to_csv('tableau_cazy.csv', index=False)

print('Tableau enregistré avec succès !')

def csv_to_xlsx():
    df= pd.read_csv('tableau_cazy.csv')
    df.to_excel('tableau_cazy.xlsx', index=False)
    print('Tableau enregistré sous format excel !')
csv_to_xlsx()

############################################################################
# url = "https://rest.uniprot.org/idmapping/run"
# data = {
#     "from": "UniProtKB_AC-ID",
#     "to": "UniRef50",
#     "ids": "Q2TYW1",
#     "types": "application",
#     "format": "json"
# }
#
# response = requests.post(url, data=data)
#
# if response.status_code == 200:
#     with open("results.xlsx", "wb") as f:
#         f.write(response.content)
#     print("Results saved to results.xlsx")
# else:
#     print(f"Error {response.status_code}: {response.text}")


