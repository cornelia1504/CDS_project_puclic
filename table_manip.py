"""Ce script contient les fonctions necessaires à la gestion des tableaux"""
import pandas as pd
import os
import io
import requests
def accession_nb_list():
    """Extraction des numéros d'accession d'uniprot
    qui correspondent aux IDs de cazy db"""
    #Lecture du fichier excel
    global file1
    file1 = input("Veuillez enter le nom du fichier ou le chemin d'accès : ")
    read_file = pd.read_excel(file1)

    #Extraction des numéros d'accession
    accession_numbers = read_file['Entry'].tolist()
    #print(accession_numbers)
    with open('accession_numbers.txt', 'w') as f:
        for accession_numbers in accession_numbers :
            f.write(accession_numbers + '\n')
    #/home/guest/Documents/Cornelia/cds_project/GH62/id_mapping/id_map_GH62_unKB.xlsx

def accession_nb_list():
    """Extraction des numéros d'accession d'uniprot
    qui correspondent aux IDs de cazy db"""
    #Lecture du fichier excel
    global file1
    file1 = input("Veuillez enter le nom du fichier ou le cemin d'accès : ")
    read_file = pd.read_excel(file1)

    #Extraction des numéros d'accession
    accession_numbers = read_file['Entry'].tolist()
    #print(accession_numbers)
    with open('accession_numbers.txt', 'w') as f:
        for accession_numbers in accession_numbers :
            f.write(accession_numbers + '\n')
    #/home/guest/Documents/Cornelia/cds_project/GH62/id_mapping/id_map_GH62_unKB.xlsx

def get_repository():
    # Obtenir le répertoire de travail actuel
    current_dir = os.getcwd()
    print("Le répertoire de travail actuel est : ", current_dir)

    # Localiser le fichier accession_numbers.txt
    file_path = os.path.join(current_dir, "accession_numbers.txt")
    print("Le fichier accession_numbers se trouve dans le répertoire : ", file_path)

    # Chemin absolu du fichier Excel
    excel_file_path = file1 #os.path.abspath("nom_du_fichier_excel.xlsx")

    # Lecture du fichier Excel
    read_file = pd.read_excel(excel_file_path)

    # Extraction des numéros d'accession
    accession_numbers = read_file['Entry'].tolist()

    # Création du chemin absolu du fichier accession_numbers.txt
    output_file_path = os.path.join(os.path.dirname(excel_file_path), "accession_numbers.txt")

    # Ecriture des numéros d'accession dans le fichier txt
    with open(output_file_path, "w") as f:
        for accession_number in accession_numbers:
            f.write(accession_number + "\n")

    print("Le fichier accession_numbers.txt a été enregistré dans le répertoire : " + os.path.dirname(excel_file_path))
def accession_nb_uni50():
    """mapping d' accession_numbers.txt contre uniref50 """
    #url = 'https://rest.uniprot.org/idmapping/run'
    url = 'https://www.uniprot.org/uploadlists/'
    with open('accession_numbers.txt') as f:
        accession_numbers = f.read().strip().split('\n')

    params = {
        'from': 'UniProtKB_AC-ID',
        'to': 'UniRef50',
        #'format': 'tab',
        'ids': ' '.join(accession_numbers)
    }

    response = requests.get(url, params=params)

    # Utilisation de io.StringIO pour créer un objet file-like à partir des données de réponse
    file_like_object = io.StringIO(response.content.decode())

    # Utilisation de l'objet file-like avec pd.read_csv
    df = pd.read_csv(file_like_object, sep='\t')

    df.to_excel('accession_numbers_uniref50.xlsx', index=False)




if __name__ == '__main__' :
    accession_nb_list()
    get_repository()
    accession_nb_uni50()
