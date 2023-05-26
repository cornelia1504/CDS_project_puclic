# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on mai 2023

@author: Mamitiana Mahitasoa
"""
import csv
import os
import alphafold as alf
import pandas as pd
###############################################################################
def extract_result(family):
    print('***********extract_result***********')
    file = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/R_all_vs_all.txt'
    data = []
    with open(file, newline='') as file:
        reader =  csv.reader(file, delimiter='\t')
        compteur = 0
        for row in reader:
            if compteur >= 11 and row[0].startswith('TRANS'):
            #if compteur >= 11 and row[0].startswith('DIST'):

                data.append(row)
            elif row[0].startswith('#'):
                compteur += 1
    output = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/res_trans_pdb_clean_alf.txt'
    #output ='res_trans.txt'
    with open(output, 'w') as f:
        for line in data:
            line_str = '\n'.join(line) + '\n'
            f.write(line_str)
    return output
def extract_scores(family):
    print('***********extract_scores***********')
    file = extract_result(family)
    with open(file, 'r'):
        col_names = ['0', '1', '2','score1', 'score2', 'pairs', '5', '6', '7',
                     '8', '9', '10', '11', '12','13','14','15','16','17','18','19']
        df = pd.read_table(file, sep='\s+', header=None)
        df.columns = col_names
        df = df.drop(['0', '1', '2','5', '6', '7', '8', '9', '10', '11', '12',
                      '13','14','15','16','17','18','19',], axis=1)
        output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/score_trans_for_matrix.txt'
        df.to_csv(f'{output_folder}', header=True, sep='\t', index=False)
        return df

########################################################################
def tableau_score(family):
    print('***********tableau_score***********')
    file = extract_result(family)
    bad_model = []
    nb_models = 0
    pairs = 0
    m_pairs = 0
    #file = '/home/guest/Documents/Cornelia/cds_project/GH128/TRUE/maxcluster/res_trans_pdb_clean_alf.txt'
    # with open(file, 'r'):
    with open(file, 'r'):
        col_names = ['0', 'id_pdb1', 'id_pdb2', 'score1', 'score2', 'pairs', '5', '6',
                     '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
        df = pd.read_table(file, sep='\s+', header=None)
        df.columns = col_names
        df = df.drop(['0', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                      '16', '17', '18', '19', ],axis=1)
        print(df)
        df_pdb = pd.DataFrame(df)
        print(df_pdb)
        # nb_residus = int(df_pdb.shape[0])
        # Parcourir chaque ligne du DataFrame
        for index, row in df_pdb.iterrows():
            if row['id_pdb1'] == 1:
                nb_models += 1
                pairs += int(row['pairs'])
        m_pairs = pairs / nb_models
        m_pairs = m_pairs / 2
        for index, row in df_pdb.iterrows():
            if row['id_pdb1'] == 1:
                if row['pairs'] < m_pairs:
                    print(int(row['id_pdb2']))
                    print('*',int(row['pairs']))
                    bad_model.append(int(row['id_pdb2']))
            else:
                pass

        print(nb_models)
        print(pairs)
        print(m_pairs)
        print(bad_model)

        output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/table_for_matrix_p_c_alf.txt'
        df.to_csv(f'{output_folder}', header=False, sep='\t', index=False)
        # error_file = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/'
        # with open(error_file + "models_frgt.txt", "w") as output_file:
        #     output_file.write('Les modèles ci-après on été écartés lors de la création de la matrice : ' + str(bad_model))

        return df, bad_model

def extract_pd_name(family):
    print('***********extract_pd_name***********')
    file = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/R_all_vs_all.txt'
    data = []
    with open(file, newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        compteur = 0
        for row in reader:
            if compteur >= 7 and row[0].startswith('PDB'):
                data.append(row)
            elif row[0].startswith('#'):
                compteur += 1

                #############################
    output = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/table_name_pdb_clean_alf.txt'
    # output ='res_trans.txt'
    with open(output, 'w') as f:
        for line in data:
            line_str = '\n'.join(line) + '\n'
            f.write(line_str)
                #############################
    file = output
    bad_models = tableau_score(family)[1]
    no_mx = []
    with open(file, 'r') as f:
        id_pdb= []
        pdb_code = []
        for line in f.readlines():
            # Séparation de la ligne en colonnes
            columns = line.strip().split()
            if int(columns[2]) not in bad_models:
                # Extraction des numéros d'accession
                id = columns[3] #accession pdb
                id = id[0:11]
                id_pdb.append(columns[2])
                pdb_code.append(id)#pdb_code.append(columns[3])
            else:
                no_mx.append(columns[3][0:11])


    #dictionnaire clé= accession_uniprot et valeur = accession_cazy
    dico_accession_pdb = dict(zip(id_pdb, pdb_code))
    print(dico_accession_pdb)
    print('bad_models : ', no_mx)
    return dico_accession_pdb, no_mx
def built_matrix_max(family):
    print('************* built_matrix_max **************')
    # Initialisation des variables
    max_scores = None
    mx = {}
    id = {}
    z = 0
    size = None
    na = 0
    # Ouverture du fichier en entrée
    with open(f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/table_for_matrix_p_c_alf.txt', 'r') as f:
        # Traitement des lignes du fichier
        for line in f:
            # Séparation de la ligne en colonnes
            columns = line.strip().split()
            max_scores = max(columns[2], columns[3])
            # Mise à jour du tableau mx
            distance = round(1.0 - float(max_scores), 8)  ### 6
            mx[columns[0] + "," + columns[1]] = distance
            mx[columns[1] + "," + columns[0]] = distance

            # Mise à jour du tableau id
            if columns[0] not in id.values():
                z += 1
                id[z] = columns[0]

            # Mise à jour de la variable size
            size = columns[0]
            # Mise à jour de max_score
            max_scores = None

    # Affichage des résultats  avec les bons accessions :
    # print(size)
    # print(mx)
    dico = extract_pd_name(family)
    # print(dico)
    dico_accession_alf = alf.retrieve_alf(family)[0]
    for x in range(1, int(size) + 1):
        if str(x) in dico:
            # pdb = dico[str(x)]
            pdb1 = dico[str(x)]
            pdb = str(pdb1).split('_')[0]
            for cle, valeur in dico_accession_alf.items():
                if valeur == pdb:
                    pdb = valeur + '*'
            # print(pdb)
            print(pdb, end=' ')
            for y in range(1, int(size) + 1):
                if str(y) in dico:
                    print(str(mx[str(x) + "," + str(y)]), end=' ')
            print()
        else:
            na += 1
    # sauvegarder la matrice
    with open(f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/matrix_max_{family}.txt', 'w') as f:
        f.write(str((int(size) - int(na))))
        f.write('\n')
        for x in range(1, int(size) + 1):
            if str(x) in dico:
                # pdb = dico[str(x)]
                pdb1 = dico[str(x)]
                pdb = str(pdb1).split('_')[0]
                for cle, valeur in dico_accession_alf.items():
                    if valeur == pdb:
                        pdb = valeur + '*'
                print(pdb, end='\t', file=f)
                for y in range(1, int(size) + 1):
                    if str(y) in dico:
                        print(str(mx[str(x) + "," + str(y)]), end='\t', file=f)
                print('\n', file=f)
    with open(f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/matrix_max_{family}.txt', 'r') as f, \
            open(f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/matrix_max_{family}lite.txt',
                 'w') as outfile:
        for i in f.readlines():
            if not i.strip():
                continue
            if i:
                outfile.write(i)
########################################################################
def fastme(family):
    print('************* fastme **************')
    file = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/matrix_max_{family}lite.txt'
    output = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/matrix_max_{family}lite_tree.nwk'
    output0 = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/matrix_max_{family}lite_tree0.nwk'
    os.system(f'fastme -o {output} -i {file }')
    #Remplacer les valeurs négatives par 0
    os.system(f"sed -e 's,:-[0-9\.]\+,:0.0,g' {output} > {output0}")
    print('******* Tree file : ', os.path.basename(output), '*******')
    print('\n *********** Thank you for using this program **********')

########################################################################

if __name__ == "__main__":
    family = input('***family*** : ')
    extract_result(family)
    extract_scores(family)
    tableau_score(family)
    extract_pd_name(family)
    # time.sleep(6)
    #map_acc_org(family)
    built_matrix_max(family)
    fastme(family)
