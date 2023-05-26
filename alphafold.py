# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on mai 2023

@author: Mamitiana Mahitasoa

Main script to retrieve pdb files for a given list of acccession
"""

import os
import pandas as pd
from biopandas.pdb import PandasPdb
import uniprot_id_mapping as map
import re

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

def search_accession_alf(family):
    print('**********search accession************')
    #family= input('family GH :')
    results = map.id_mapping_uniprot_uniref50(family)
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
            file = f'{key}_cluster50.list'
            print(file)
            file = f'/home/guest/Documents/Cornelia/cds_project/{family}' \
                   f'/clean_info_{family}/list_accession_clt50/{file}'
            #os.mkdir(file)
            print('*************************')
            os.system(f'wget -q -O {file} https://rest.uniprot.org/uniref/{cluster}'
                      f'/members?format=list&size=500 > {file}')
            if os.path.isfile(file):
                print(f"Le fichier {file} a été téléchargé avec succès.")
                cluster_files_list.append(file)
            else:
                print(f"Une erreur est survenue lors du téléchargement de {file}.")
    print('code_alf : ', code_alf)
    print('********', len(code_alf))

    print('code_alf_dwl :', code_alf_dwl)
    print('********', len(code_alf_dwl))

    print(cluster_files_list)
    return cluster_files_list, code_alf, code_alf_dwl

#/home/guest/Documents/Cornelia/cds_project/script/clean_script/A0A059U4D1_cluster50.list

def retrieve_alf(family):
    all_accession_alf = []
    no_alf_acs = []
    directory = f'/home/guest/Documents/Cornelia/cds_project/{family}/list_accession_clt50'#

    if not os.path.exists(directory):
        os.mkdir(directory)
    file_names = os.listdir(f'{directory}')
    dico_accession_alf = {}
    for name in file_names:
        file = f'{directory}/{name}'
        with open(f'{file}', 'r') as f:
            accession_alf_list = []
            for line in f.readlines():
                pattern = r"\b\w{6}(?=_)"
                regex = re.compile(pattern)
                result = regex.findall(line)
                if result:
                    dico_accession_alf[name[0:9]] = result[0]
                    accession_alf_list.append(result[0])
                    break  # sortir de la boucle dès qu'on trouve l'accession à 6 caractères
            if accession_alf_list:
                premier_element = accession_alf_list[0]
            else:
                print("Fichier ", file ," \n La liste est vide !")
                premier_element = None
                no_alf_acs.append(name[0:10])
            if premier_element != None:
                all_accession_alf.append(premier_element)
    # print('dico : ', dico_accession_alf)
    # print('liste finale : ',all_accession_alf)
    print('**** Accession trouvée pour ', len(all_accession_alf),' clusters *****')
    print('**** Aucune accession trouvée pour ', len(no_alf_acs),' clusters *****')

    #download pdb filees
    output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/modeles_alph_clt'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for file_name, accession in dico_accession_alf.items():
        output_file = os.path.join(output_folder, f"{file_name}_al.pdb")
        output_file = os.path.join(output_folder, f"{accession}_al.pdb")

        os.system(f'wget -O {output_file} https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v4.pdb')
        #https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-model_v4.pdb

    print('dico : ',dico_accession_alf)
    return dico_accession_alf, all_accession_alf


#########################################################################

#########################################################################
def download_models(family):
    """function to retrieve alphafold modeles pdb files of a list of accession"""
    global output_folder
    output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_info_{family}/modeles_alf_clt'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # accession_search = retrieve_alf(family)
    # dico_accessions = accession_search[0]
    search_accession = map.search_accession_alf_50(family)
    code_alf = search_accession[1]
    code_alf_dwl = search_accession[2]
    print('**************************** \n')
    retieve = retrieve_alf(family)
    all_accession_alf = retieve[1]
    dwl_accessions = code_alf.__str__() + all_accession_alf.__str__()
    print('\n **** code_alf accessions : ', code_alf)
    print(len(code_alf))
    print('\n **** all accessions : ', all_accession_alf)
    print(len(all_accession_alf))
    print('\n **** dwl accessions : ', dwl_accessions)
    print(len(dwl_accessions))

def clean_alf_bis(family):
    models_folder = os.listdir(f'/home/guest/Documents/Cornelia/cds_project/{family}/modeles_alph_clt')
    models = []
    for i in models_folder:
        models.append(f'/home/guest/Documents/Cornelia/cds_project/{family}/modeles_alph_clt/{i}')
    for pdb in models:
        if os.path.getsize(pdb) > 0:
            pdb_file = pdb
            pdb_accession = os.path.basename(pdb_file)
            pdb_accession = pdb_accession[0:9]  #à corriger
            ppdb = PandasPdb()
            ppdb.read_pdb(pdb_file)
            df_pdb = ppdb.df['ATOM']
            #print(df_pdb)
            ###################
            '''Select regions with pLDDT score of 50 or above'''
            results_df = df_pdb[df_pdb['b_factor'].astype(float) >= 70] #############

            '''Write novel pdb file'''
            output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_pdb_alph70'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            fh_pdb = open(f'{output_folder}/{pdb_accession}.pdb', 'w')
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
        else:
            print(os.path.basename(pdb), 'est vide')
    print("\n Modèles traités avec succès !")
def compte_pdb_files():
    directory = output_folder
    pdb_files = os.listdir(directory)

    nb_files = len(pdb_files)
    print(f'{nb_files} modèles télécharger sur {compteur} accessions pdb')
###############################################################################
def clean_alf(family):
    """  """
    bad_models = 0
    models_folder = os.listdir(f'/home/guest/Documents/Cornelia/cds_project/{family}/modeles_alph_clt')
    models = []
    for i in models_folder:
        models.append(f'/home/guest/Documents/Cornelia/cds_project/{family}/modeles_alph_clt/{i}')
    for pdb in models:
        if os.path.getsize(pdb) > 0:
            score = 0
            global_score = 0
            nb_residus = 0
            pdb_file = pdb
            pdb_accession = os.path.basename(pdb_file)
            pdb_accession = pdb_accession[0:9]  #à corriger
            ppdb = PandasPdb()
            ppdb.read_pdb(pdb_file)
            df_pdb = ppdb.df['ATOM']
            print('df ',df_pdb)####
            df_pdb = pd.DataFrame(df_pdb)
            #nb_residus = int(df_pdb.shape[0])
            # Parcourir chaque ligne du DataFrame
            for index, row in df_pdb.iterrows():
                if row['atom_name'] == 'CA':
                    nb_residus += 1
                    # Accéder à la valeur de la colonne 'b_factor' pour chaque ligne
                    b_factor = row['b_factor']
                    # Incrémenter le compteur avec la valeur de la colonne
                    score += b_factor
            print('nb_residus', nb_residus)
            print(score)
            global_score = score / nb_residus
            print(global_score)
            ###################
            if global_score >= 70 :
                '''Select regions with pLDDT score of 50 or above'''
                results_df = df_pdb[df_pdb['b_factor'].astype(float) >= 70] #############

                '''Write novel pdb file'''
                output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/clean_pdb_alph70'
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                fh_pdb = open(f'{output_folder}/{pdb_accession}.pdb', 'w')
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
            else:
                bad_models += 1
                print('score du modèle faible pour : ', os.path.basename(pdb))
                print('Global plDDT : ', global_score)
        else:
            print(os.path.basename(pdb), 'est vide')
    print("\n Modèles traités avec succès !")
    print('nb bad_models: ', bad_models)
    return bad_models

#############
if __name__ == "__main__":
    family = input('famille : ')
    print('**')
    #search_accession_alf(family)
    #retrieve_alf(family)
    #download_models(family)
    print('**')
    #download_pdb()
    #clean_alf(family)
    #compte_pdb_files()
    clean_alf(family)