"""Main script to retrieve alphafold predication for a given list of acccession """

import pandas as pd
#/home/guest/Documents/Cornelia/cds_project/GH62/id_mapping/id_map_GH62_unKB.xlsx
accessions = []
def ids_for_alph():
    file_path = input('Entrez le chemin vers votre fichier : ')
    with open(file_path, 'r') as f:
        accession = f.readlines()
        for line in accession:
            if len(line.strip())==6:
                accessions.append(line.strip())
    print(accessions)

def compte_ids():
    compteur= 0
    for i in accessions:
        compteur += 1
    return compteur
    print(compteur)
    print('Test')

if __name__ == "__main__":
    ids_for_alph()
    compte_ids()

