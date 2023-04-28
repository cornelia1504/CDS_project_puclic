import csv
import pandas as pd
###############################################################################
#/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/R_test_A_f_R2.txt
def extract_result():
    file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/R_maxc_ava_2_GH62.txt'
    #file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/R_test_A_1.txt'
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
    output = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/res_trans_pdb_clean_alf.txt'
    #output ='res_trans.txt'
    print(type(data))
    with open(output, 'w') as f:
        for line in data:
            line_str = '\n'.join(line) + '\n'
            print(line_str)
            f.write(line_str)
    #print(data)
    print(compteur)
    return output

def fextract_pd_name():
    file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/R_maxc_ava_3_GH62.txt'
    data = []
    with open(file, newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        compteur = 0
        for row in reader:
            if compteur >= 7 and row[0].startswith('PDB'):
                data.append(row)
            elif row[0].startswith('#'):
                compteur += 1
    output = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/R_maxc_ava_3_GH62.txt'
    file = output
    with open(file, 'r') as f:
        id_pdb= []
        pdb_code = []
        for line in f.readlines():
            # Séparation de la ligne en colonnes
            columns = line.strip().split()
            # Extraction des numéros d'accession
            print('#################################')
            print(columns)
            print(columns[2])
            id_pdb.append(columns[2])
            pdb_code.append(columns[3])
    #print(id_pdb, '=', pdb_code)
    #dictionnaire clé= accession_uniprot et valeur = accession_cazy
    dico_accession_pdb = dict(zip(id_pdb, pdb_code))
    print(dico_accession_pdb)
    return dico_accession_pdb
def extract_pd_name():
    file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/R_maxc_ava_2_GH62.txt'
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
    output = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/table_name_pdb_clean_alf.txt'
    # output ='res_trans.txt'
    print(type(data))
    with open(output, 'w') as f:
        for line in data:
            line_str = '\n'.join(line) + '\n'
            print(line_str)
            f.write(line_str)
        # print(data)
        print(compteur)
                #############################
    file = output
    with open(file, 'r') as f:
        id_pdb= []
        pdb_code = []
        for line in f.readlines():
            # Séparation de la ligne en colonnes
            columns = line.strip().split()
            # Extraction des numéros d'accession
            print('#################################')
            print(columns)
            print(columns[2])
            id_pdb.append(columns[2])
            pdb_code.append(columns[3])
    #dictionnaire clé= accession_uniprot et valeur = accession_cazy
    dico_accession_pdb = dict(zip(id_pdb, pdb_code))
    print(dico_accession_pdb)
    return dico_accession_pdb
def extract_scores():
    file = extract_result()
    with open(file, 'r'):
        col_names = ['0', '1', '2','score1', 'score2', 'pairs', '5', '6', '7', '8', '9', '10', '11', '12','13','14','15','16','17','18','19']
        df = pd.read_table(file, sep='\s+', header=None)
        print(df)
        df.columns = col_names
        df = df.drop(['0', '1', '2','5', '6', '7', '8', '9', '10', '11', '12','13','14','15','16','17','18','19',], axis=1)
        print(df)
        output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/score_trans_for_matrix.txt'
        df.to_csv(f'{output_folder}', header=True, sep='\t', index=False)
        return df

def tableau_score():
    file = extract_result()
    with open(file, 'r'):
        col_names = ['0', 'id_pdb1', 'id-pdb2', 'score1', 'score2', 'pairs', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
                     '15', '16', '17', '18', '19']
        df = pd.read_table(file, sep='\s+', header=None)
        print(df)
        df.columns = col_names
        df = df.drop(
            ['0', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', ],
            axis=1)
        print(df)
        output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/table_for_matrix_p_c_alf.txt'
        df.to_csv(f'{output_folder}', header=False, sep='\t', index=False)
        return df

def max_score():
    tableau = tableau_score()
    max =   None
    dist = None
    for i in tableau['score1']:
        x= i
    for i in tableau['score2']:
        y= i
        print(y)
    #print(tableau)
########################################################################
def built_matrix():
    # Initialisation des variables
    max_scores = None
    mx = {}
    id = {}
    z = 0
    size = None

    # Ouverture du fichier en entrée
    with open('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/table_for_matrix_p_c_alf.txt', 'r') as f:
        # Traitement des lignes du fichier
        for line in f:
            # Séparation de la ligne en colonnes
            columns = line.strip().split()
            print(columns)
            # Mise à jour de la variable small
            # max_scores = columns[2] #ligne changée
            # if max_scores is None or columns[3] < max_scores:
            #     max_scores = columns[3] #2 avant
            # #max_scores = max(columns[2],columns[3])
            max_scores = float(columns[2]) +float(columns[3])
            max_scores =max_scores/2
            print(max_scores)
            # Mise à jour du tableau mx
            distance= round(1.0 - float(max_scores),6) ###
            print(distance)
            mx[columns[0] + "," + columns[1]] = distance
            mx[columns[1] + "," + columns[0]] = distance

            # Mise à jour du tableau id
            if columns[0] not in id.values():
                z += 1
                id[z] = columns[0]

            # Mise à jour de la variable size
            size = columns[0]
            #Mise à jour de max_score
            max_scores = None

    # # Affichage des résultats
    # print(size)
    # for x in range(1, int(size) + 1):
    #     print("pdb" + str(id[x]), end=' ')
    #     for y in range(1, int(size) + 1):
    #         print(str(mx[str(x) + "," + str(y)]), end=' ')
    #     print()

    # Affichage des résultats  avec les bons accessions :
    print(size)
    print(mx)
    dico = extract_pd_name()
    for x in range(1, int(size) + 1):
        pdb = dico[str(x)]
        #print(pdb)
        print(pdb, end=' ')
        for y in range(1, int(size) + 1):
            print(str(mx[str(x) + "," + str(y)]), end=' ')
        print()
    # sauvegarder la matrice
    with open('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/matrix_3d_p_c_alf_GH62.txt', 'w') as f:
        f.write(size+ '\n')
        for x in range(1, int(size) + 1):
            pdb = dico[str(x)]
            print(pdb, end='\t', file=f)
            for y in range(1, int(size) + 1):
                print(str(mx[str(x) + "," + str(y)]), end='\t', file=f)
            print('\n', file=f)
    with open('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/matrix_3d_p_c_alf_GH62.txt', 'r') as f,\
            open('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/matrix_3d_p_c_alf_GH62_lite.txt', 'w') as outfile:
        for i in f.readlines():
            if not i.strip():
                continue
            if i:
                outfile.write(i)
########################################################################
def extract_scores2():
    file = extract_result()
    with open(file, 'r'):
        col_names = ['0', '1', '2','3','score']
        df = pd.read_table(file, sep='\s+', header=None)
        print(df)
        df.columns = col_names
        df = df.drop(['0', '1', '2','3'], axis=1)
        print(df)
        output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/score_DIST_for_matrix.txt'
        df.to_csv(f'{output_folder}', header=True, sep='\t', index=False)
        return df

def tableau_score2():
    file = extract_result()
    with open(file, 'r'):
        col_names = ['0', '1','id_pdb1', 'id-pdb2', 'score']
        df = pd.read_table(file, sep='\s+', header=None)
        print(df)
        df.columns = col_names
        df = df.drop(
            ['0','1'],axis=1)
        print(df)
        output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/table_DIST_for_matrix_p_c_alf.txt'
        df.to_csv(f'{output_folder}', header=False, sep='\t', index=False)
        return df

def built_matrix2():
    # Initialisation des variables
    max_scores = None
    mx = {}
    id = {}
    z = 0
    size = None

    # Ouverture du fichier en entrée
    with open('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/table_DIST_for_matrix_p_c_alf.txt', 'r') as f:
        # Traitement des lignes du fichier
        for line in f:
            # Séparation de la ligne en colonnes
            columns = line.strip().split()
            # Mise à jour de la variable maxscore
            max_scores = columns[2]

            # Mise à jour du tableau mx
            distance= round(100 - float(max_scores),6) ###
            print(distance)
            distance= round(distance * float(0.01),6) ###
            print(distance)
            mx[columns[0] + "," + columns[1]] = distance
            mx[columns[1] + "," + columns[0]] = distance

            # Mise à jour du tableau id
            if columns[0] not in id.values():
                z += 1
                id[z] = columns[0]

            # Mise à jour de la variable size
            size = columns[0]
            #Mise à jour de max_score
            max_scores = None

    # Affichage des résultats  avec les bons accessions :
    print(size)
    print(mx)
    dico = extract_pd_name()
    for x in range(1, int(size) + 1):
         pdb = dico[str(x)]
        #print(pdb)
         print(pdb, end=' ')
         for y in range(1, int(size) + 1):
             print(str(mx[str(x) + "," + str(y)]), end=' ')
         print()
    # sauvegarder la matrice
    with open('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/matrix_3_p_c_alf_GH62.txt', 'w') as f:
        f.write(size+ '\n')
        for x in range(1, int(size) + 1):
            pdb = dico[str(x)]
            print(pdb, end='\t', file=f)
            for y in range(1, int(size) + 1):
                print(str(mx[str(x) + "," + str(y)]), end='\t', file=f)
            print('\n', file=f)
    with open('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/matrix_3_p_c_alf_GH62.txt', 'r') as f,\
            open('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/matrix_3_p_c_alf_GH62_lite.txt', 'w') as outfile:
        for i in f.readlines():
            if not i.strip():
                continue
            if i:
                outfile.write(i)
########################################################################

if __name__ == "__main__":
    # extract_result()
    # extract_scores()
    # tableau_score()
    #extract_pd_name()
    #max_score()
    built_matrix()
    #built_matrix2()