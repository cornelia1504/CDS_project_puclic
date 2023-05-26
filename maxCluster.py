# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on mai 2023

@author: Mamitiana Mahitasoa

maxcluster
"""
from Bio.PDB import PDBParser, PDBIO
import clustering as clt
parser = PDBParser()
import shutil
import os
from datetime import datetime

#class Maxcluster:
maxcluster = '/home/guest/Documents/Cornelia/cds_project/MAXCLUSTER/maxcluster64bit'
def merge_files(family):
    print('\n', '******************** merge_files ************************', '\n')
    representant = clt.Pisces(family)

    # Liste des noms des fichiers PDB à assembler
    repertoire_source1 = f"/home/guest/Documents/Cornelia/cds_project/{family}/clean_pdb_A"
    repertoire_source2 = f"/home/guest/Documents/Cornelia/cds_project/{family}/clean_pdb_alph70"
    repertoire_destination = f"/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/all_pdb"

    # Vérifier si le répertoire de destination existe déjà
    if os.path.exists(repertoire_destination):
        # Renommer le répertoire de destination existant
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        repertoire_destination_backup = f"{repertoire_destination}_backup_{timestamp}"
        os.rename(repertoire_destination, repertoire_destination_backup)

    # Créer le répertoire de destination
    os.makedirs(repertoire_destination)

    # Copier les fichiers des répertoires source vers le répertoire de destination
    copy_selected_files(repertoire_source1, repertoire_destination, representant)
    copy_files(repertoire_source2, repertoire_destination)


def copy_selected_files(source_directory, destination_directory, selected_files):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if any(rep in file for rep in selected_files):
                source_file = os.path.join(root, file)
                shutil.copy2(source_file, destination_directory)


def copy_files(source_directory, destination_directory):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            source_file = os.path.join(root, file)
            shutil.copy2(source_file, destination_directory)


#/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/pdb_alphaf
def fichier_pdb():
    # Liste des noms des fichiers PDB à assembler
    global pdb_files
    global pdb_files_list
    pdb_files = []
    directory = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/pdb_alphaf'
    pdb_files_list = os.listdir(directory)
    print(pdb_files_list)
    for pdb in pdb_files_list:
        pdb_files.append(directory + '/' +pdb)
    compteur = 0
    for i in pdb_files_list:
        compteur += 1
    print(compteur)
    print(pdb_files)
    return pdb_files, compteur

def pairwaise(pdb_files):
    """module to compare pdb files all verses all"""
    prediction_file = pdb_files
    #pdb_files.reverse()
    experiment_file = pdb_files
    #print(experiment_file)
    fichier_log = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/pairwise.log'
    for i in prediction_file:
        for j in experiment_file:
            print('Comparaison ',os.path.basename(i), 'VS',os.path.basename(j))
            #os.system(f'{maxcluster} -e {i} -p {j} -in -matrix -log {fichier_log}')
            os.system(f'{maxcluster} -e {i} -p {j} -in -matrix -log {fichier_log} '
                      f'-R distance_pairwise.txt -Rl lite_distance_pw.txt')

            #os.system(f'{maxcluster} -e {i} -p {j} -o ascii -g distance_matrix.txt')
    #return prediction_file

def all_vs_all_bis(family):
    """module to compare pdb files all verses all"""
    print('\n','******************** all_vs_all ************************', '\n')
    #/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/PDB_all_models
    paths = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/PDB_all_models/'
    files = os.listdir(f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/PDB_all_models')
    #files = os.listdir(paths)
    list_pdb_paths = []
    for file in files :
        list_paths = f'{paths}{file}'
        #print(list_paths)
        list_pdb_paths.append(list_paths)
        # print(list_pdb_paths)
        list_file = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/list_file.txt'
        with open(list_file, 'w') as l:
            l.write('\n'.join(list_pdb_paths))
        ##############################################
        # os.system(f'cd /home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/')
        list_file_path = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/list_2pdb_af.txt'
        fichier_log = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/all_vs_all.log'
        fichier_R = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/R_all_vs_all.txt'

        with open(list_file_path, 'w') as c:
            c.write('\n'.join(files))
        # os.system(f'cd {paths}')
        # os.system(f'cd {paths} | {maxcluster} -l {list_file_path} -log {fichier_log}')
        ##############################################

        # print('Comparaison ',os.path.basename(files))
    os.system(
            f"cd /home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/PDB_all_models && ls")
        # os.system(
        #     f"cd /home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/PDB_all_models | "
        #     f"{maxcluster} -l {list_file} -TM -log {fichier_log} -R {fichier_R}")

def all_vs_all(family):
    """module to compare pdb files all verses all"""
    print('\n','******************** Maxcluster all_vs_all ************************', '\n')
    max_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster'
    if not os.path.exists(max_folder):
        os.mkdir(max_folder)
    paths = f"/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/all_pdb/"
    files = os.listdir(f"/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/all_pdb")
    #files = os.listdir(paths)
    list_pdb_paths = []
    for file in files:
        list_paths = f'{file}'
        list_pdb_paths.append(list_paths)

    list_file = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/list_file.txt'
    with open(list_file, 'w') as l:
        l.write('\n'.join(list_pdb_paths))

    list_file_path = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/list_2pdb_af.txt'
    fichier_log = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/all_vs_all.log'
    fichier_R = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/R_all_vs_all.txt'

    # with open(list_file_path, 'w') as c:
    #     c.write('\n'.join(files))

    print('\n Comparaison en cours ... \n')
    # os.system(f"cd /home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/all_pdb && "
    #           f"{maxcluster} -l {list_file} -in -TM -log {fichier_log} -R {fichier_R}")
    os.system(f"cd /home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/all_pdb && "
              f"{maxcluster} -l {list_file} -in -TM -mP 20 -i 4 -log {fichier_log} -R {fichier_R}")
    # os.system(f"cd /home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/all_pdb && "
    #           f"{maxcluster} -l {list_file} -in -rankMS -mP 20 -i 4 -log {fichier_log} -R {fichier_R}")

def list_processing():
    print('\n','********************************************', '\n')
    print('list_processing')
    print('\n','********************************************', '\n')
    list_file = 'list_file.txt'
    id = pdb_files_list
    print(id)
    fichier_log = []
    for accession in id:
        fichier_log.append(f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/fichier_log/list_processing_{accession}.log')
    print(fichier_log)
    repository = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/clean_pdb_A_maxcluster'
    for pdb in pdb_files:
        for log in fichier_log:
            id_pdb =os.path.basename(pdb)[:4]
            print(id_pdb)
            #print(log)
            id_log = os.path.basename(log)[16:20]
            print(id_log)
            if id_pdb == id_log:
            #print(pdb)
                os.system(f'cd {repository} | {maxcluster} -e {pdb} -l {list_file} -in -matrix -log {log} > list_processig.txt')
            #os.system(f'{maxcluster} -e {pdb} -l {list_file} -in -matrix -log {fichier_log} -R distance_pairwise.txt -Rl lite_distance_pw.txt')


if __name__ == "__main__":
    # pdb_files_compteur = fichier_pdb()
    # pdb_files = pdb_files_compteur[0]
    # compteur = pdb_files_compteur[1]
    #pairwaise(pdb_files)
    #merge_files()
    family = input('fam?')
    #compteur_t(all_veres_all(family))
    #all_vs_all_bis(family)
    all_vs_all(family)
    #merge_files(family)
    #compteur_t(list_processing())
    #list_processing()
