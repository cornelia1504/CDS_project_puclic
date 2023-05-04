"""Main script to retrieve pdb files for a given list of acccession """

import os
import time
from biopandas.pdb import PandasPdb

#/home/guest/Documents/Cornelia/cds_project/GH62/id_mapping/id_map_GH62_unKB.xlsx
accessions = []
accession2 = []
def ids_for_alph():
    file_path = 'accession_nb.txt'
    file_path = 'accession_nb.txt'

    with open(file_path, 'r') as f:
        accession = f.readlines()
        accession2 =f.readlines()
        for line in accession:
            if len(line.strip())==6:
                accessions.append(line.strip())
            if len(line.strip())!=6:
                accession2.append(line.strip())
    compteur = len(accessions)
    compteur2 = len(accession2)
    #print(compteur, '/', compteur2)
    return accessions,  accession2

def compte_ids():
    global compteur
    compteur= 0
    for i in accessions:
        compteur += 1
    print('nombre d accessions avec un modèle Alphafold disponible : ',compteur)
    compteur2= ids_for_alph()
    compteur2 = len(compteur2[1])
    print('nombre d accessions avec un modèle Alphafold non disponible : ',compteur2)

def download_pdb() :
    """function to retrieve alphafold modeles pdb files of a list of accession"""
    global output_folder
    output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/modeles_alph5'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for accession in accessions:
        output_file = os.path.join(output_folder, f"{accession}_alph.pdb")
        os.system(f'wget -O {output_file} https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v4.pdb')
        #https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-model_v4.pdb

def clean_alf():
    models_folder = os.listdir('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/modeles_alph5')
    print(models_folder)
    models = []
    for i in models_folder:
        models.append(f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/modeles_alph5/{i}')
    for pdb in models:
        pdb_file = pdb
        print(pdb_file)
        pdb_accession = os.path.basename(pdb_file)
        pdb_accession = pdb_accession[0:10]
        print(pdb_accession)
        ppdb = PandasPdb()
        ppdb.read_pdb(pdb_file)
        df_pdb = ppdb.df['ATOM']
        print(df_pdb)
        ###################
        '''Select regions with pLDDT score of 50 or above'''
        results_df = df_pdb[df_pdb['b_factor'].astype(float) >= 70]

        '''Write novel pdb file'''
        output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/clean_pdb_alph70'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        fh_pdb = open(f'{output_folder}/{pdb_accession}_C70.pdb', 'w')
        results_df['bl'] = ''
        results_df['bl2'] = ''
        results_df = results_df[['record_name', 'atom_number', 'bl', 'atom_name',
                                 'residue_name', 'chain_id', 'residue_number',
                                 'bl2', 'x_coord', 'y_coord', 'z_coord',
                                 'occupancy', 'b_factor', 'element_symbol']]

        for index, row in results_df.iterrows():
            fh_pdb.write(
                '{0:5s}{1:6d} {2} {3:3s} {4:3s} {5:1s}{6:4d} {7} {8:10.3f}{9:8.3f}{10:8.3f}  {11} {12:5.2f}           {13}\n'.format(
                    row['record_name'], int(row['atom_number']), row['bl'],
                    row['atom_name'], row['residue_name'], row['chain_id'],
                    int(row['residue_number']), row['bl2'], float(row['x_coord']),
                    float(row['y_coord']), float(row['z_coord']), row['occupancy'],
                    float(row['b_factor']), row['element_symbol']))
def compte_pdb_files():
    directory = output_folder
    pdb_files = os.listdir(directory)

    nb_files = len(pdb_files)
    print(f'{nb_files} modèles télécharger sur {compteur} accessions pdb')

#############
def cluster_name(seuil):
    global output_folder
    global output_file
    output_folder = f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster{seuil}_name'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    accession2 = ids_for_alph()
    accession2 = accession2[1]
    accession_test =  accession2[200:202]
    print(accession_test)
    for accession in accession_test :
        output_file = os.path.join(output_folder, f"{accession}_cluster{seuil}.txt")
        if seuil == 50 :
            idt = 0.5
        os.system(f'wget -O {output_file} https://www.uniprot.org/uniref/?query=uniprot_id:{accession}+AND+identity:{idt}')
        os.system(f'wget -O {output_file} https://rest.uniprot.org/uniref/stream?download=true&format=list&query=%28uniprot_id%3A{accession}%20AND%20identity%3A{idt}%29')
        output_file= 'id_test.list'
        os.system(f'wget -O {output_file} https://rest.uniprot.org/uniref/stream?download=true&format=list&query=%28uniprot_id%3AA0A0H3D3A8%20AND%20identity%3A0.5%29')

        #https://rest.uniprot.org/uniref/stream?download=true&format=list&query=%28uniprot_id%3AA0A0H3D3A8%20AND%20identity%3A0.5%29

        #https://www.uniprot.org/uniref/?query=uniprot_id:P99999+AND+identity:0.5
        #https://rest.uniprot.org/uniref/stream?download=true&format=list&query=%28uniprot_id%3A{accession}%20AND%20identity%3A{idt}%29
        #https://rest.uniprot.org/uniref/stream?download=true&format=list&query=%28uniprot_id%3AP99999%20AND%20identity%3A0.5%29
        time.sleep(6)
#############
def list_cluster(seuil):
    """ """
    global output_folder
    global output_file
    output_folder = f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster{seuil}_list'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    accession2 = ids_for_alph()
    accession2 = accession2[1]
    accession_test =  accession2[200:202]
    print(accession_test)
    for accession in accession_test :
        output_file = os.path.join(output_folder, f"{accession}_cluster{seuil}.txt")
        os.system(f'wget -O {output_file} https://rest.uniprot.org/uniref/UniRef{seuil}_{accession}/members?format=list&size=500')
        time.sleep(6)
        #os.system(f'https://rest.uniprot.org/uniref/UniRef90_{i}/members?format=list&size=500')
    #     with open(output_file, 'r') as f:
    #         lignes = f.readlines()
    #         print(output_file)
    #         print(lignes)
    #         if lignes is None :
    #             os.system(
    #                 f'wget -O {output_file} https://rest.uniprot.org/uniref/UniRef{seuil}_{accession}/members?format=list&size=500')
    return output_file


def control2(seuil):
    """ """
    # files = list_cluster(50)
    # files = files[0]

    # Chemin du répertoire
    directory = f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster{seuil}_list'
    #output_folder = f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster{seuil}_list'

    # Initialisation de la liste des chemins d'accès des fichiers
    file_paths = []

    # Parcours du répertoire et stockage des chemins d'accès des fichiers
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            file_paths.append(path)

    # Affichage des chemins d'accès des fichiers
    print(file_paths)

    #print(files)
    for file in file_paths:
        accession = os.path.basename(file)
        accession = accession[0:10]
        print(accession)
        while True:
            with open(file, 'r') as f:
                lignes = f.readlines()
                print(len(lignes))
                ligne1 = len(lignes)
                print(lignes)
                if ligne1 != 1:
                    print('************************')
                    print(file)
                    os.system(
                        f'wget -O {file} https://rest.uniprot.org/uniref/UniRef{seuil}_{accession}/members?format=list&size=500')
                else:
                    print('###########################"')
                    print(file, 'OK')


def control(seuil):
    directory = f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster{seuil}_list'
    file_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if
                  os.path.isfile(os.path.join(directory, filename))]

    # Repeat the loop until all files are non-empty
    updated = True
    while updated:
        updated = False
        for file in file_paths:
            if os.path.getsize(file) == 0:
                accession = os.path.basename(file)[:10]
                print(f"Downloading {file}...")
                os.system(
                    f'wget -O {file} https://rest.uniprot.org/uniref/UniRef{seuil}_{accession}/members?format=list&size=500')
                updated = True
                time.sleep(5)
            else:
                print(f"{file} OK")
                file_paths.remove(file)  # Remove file from list to skip it in next iteration


def test(seuil):
    """ """
    #files = list_cluster(50)
    file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster90_list/A0A1C4XDE0_cluster90.txt'
    #file= '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster90_list/A0A0S2CW01_cluster90.txt'
    print(file)
    accession = os.path.basename(file)
    accession = accession[0:10]
    print(accession)
    with open(file, 'r') as f:
        lignes = f.readlines()
        print(len(lignes))
        ligne1 = len(lignes)
        print(lignes)
        if ligne1 != 1 :
            print('************************')
            os.system(f'wget -O {file} https://rest.uniprot.org/uniref/UniRef{seuil}_{accession}/members?format=list&size=500')
        else:
            print('OK')


def test2(seuil):
    file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/cluster100_list/A0A7G5J8U4_cluster100.txt'
    accession = os.path.basename(file)
    accession = accession[0:10]
    accession= 'Q2U7D2'
    os.system(f'wget -O {file} https://rest.uniprot.org/uniref/UniRef{seuil}_{accession}/members?format=list&size=500')

#https://rest.uniprot.org/idmapping/uniref/results/stream/e5cb63893b2dd929250fbb630999e214900b713b?download=true&format=list
if __name__ == "__main__":
    #ids_for_alph()
    #compte_ids()
    # download_pdb()
    # compte_pdb_files()
    #clean_alf()
    #list_cluster(100)
    #control(100)
    #test2(100)
    cluster_name(50)