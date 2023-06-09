""" maxcluster manipulation """
from Bio.PDB import PDBParser, PDBIO
import os
import time
parser = PDBParser()

#class Maxcluster:
maxcluster = '/home/guest/Documents/Cornelia/cds_project/MAXCLUSTER/maxcluster64bit'

def merge_files(self):
    # Liste des noms des fichiers PDB à assembler
    global pdb_files
    pdb_files = []
    directory = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb/'
    pdb_files_list = os.listdir(directory)
    print(pdb_files_list)
    for pdb in pdb_files_list:
        pdb_files.append(directory+pdb)
    #print(pdb_files)

    # Initialiser un objet Structure
    structure = None

    # Parcourir tous les fichiers PDB et ajouter chaque modèle à la structure
    for file in pdb_files:
        # Lire le nom de fichier
        pdb_name = os.path.basename(file)
        # Lire le fichier PDB
        pdb = parser.get_structure(pdb_name, file)
        # Parcourir chaque modèle dans le fichier PDB
        for model in pdb:
            model.id = f"{pdb_name}_{model.id}"
            #Parcourir chaque chaine dans le modèle
            #for chain in model:
            # Ajouter le modèle à la structure
            if structure is None:
                structure = model
            else:
                #model.id = f"{pdb_name}_{model.id}"
                structure.add(model)

    # Écrire la structure complète dans un seul fichier PDB
    io = PDBIO()
    io.set_structure(structure)
    io.save("all_models.pdb")


#/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb

#/home/guest/Documents/Cornelia/cds_project/MAXCLUSTER
#/home/guest/Documents/Cornelia/cds_project/MAXCLUSTER/maxcluster64bit

def fichier_pdb():
    # Liste des noms des fichiers PDB à assembler
    global pdb_files
    global pdb_files_list
    pdb_files = []
    directory = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb/'
    pdb_files_list = os.listdir(directory)
    print(pdb_files_list)
    for pdb in pdb_files_list:
        pdb_files.append(directory + pdb)
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
            os.system(f'{maxcluster} -e {i} -p {j} -in -matrix -log {fichier_log} -R distance_pairwise.txt -Rl lite_distance_pw.txt')

            #os.system(f'{maxcluster} -e {i} -p {j} -o ascii -g distance_matrix.txt')
    #return prediction_file

def all_veres_all():
    """module to compare pdb files all verses all"""
    print('\n','********************************************', '\n')
    print('all_vs_all')
    print('\n','********************************************', '\n')
    #list_file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/testAllPDB.txt'
    paths = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb/'
    files = os.listdir('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb')
    #files = os.listdir(paths)
    list_pdb_paths = []
    for file in files :
        list_paths = f'{paths}{file}'
        #print(list_paths)
        list_pdb_paths.append(list_paths)
    #print(list_pdb_paths)
    with open('list_file.txt', 'w') as l:
        l.write('\n'.join(list_pdb_paths))
    ##############################################
    #os.system(f'cd /home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/')
    list_file_path = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/list_code_file.txt'
    fichier_log = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/all_vs_all.log'
    with open(list_file_path, 'w') as c:
        c.write('\n'.join(files))
    #os.system(f'cd {paths}')
    #os.system(f'cd {paths} | {maxcluster} -l {list_file_path} -log {fichier_log}')
    ##############################################

    #print('Comparaison ',os.path.basename(files))
    os.system(f'{maxcluster} -l list_file.txt -log {fichier_log}')
    os.system(f'{maxcluster} -l list_file.txt')
    os.system(f'{maxcluster} -l list_file.txt > all_vs_all.txt')

    #os.system(f'{maxcluster} -l list_file.txt -in -matrix -log {fichier_log}')

def list_processing():
    print('\n','********************************************', '\n')
    print('list_processing')
    print('\n','********************************************', '\n')
    list_file = 'list_file.txt'
    id = pdb_files_list
    fichier_log = []
    for accession in id:
        fichier_log.append(f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/list_processing_{accession}.log')
    print(fichier_log)
    repository = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb'
    for pdb in pdb_files:
        for log in fichier_log:
            print(pdb)
            os.system(f'cd {repository} | {maxcluster} -e {pdb} -l {list_file} -in -matrix -log {log} > list_processig.txt')
            #os.system(f'{maxcluster} -e {pdb} -l {list_file} -in -matrix -log {fichier_log} -R distance_pairwise.txt -Rl lite_distance_pw.txt')
    print("ohhhh")

def compteur_t(fonction):
    start_time = time.time()
    fonction
    end_time = time.time()
    execution_time = end_time- start_time
    print('Comparaison faite en ',execution_time,'pour', compteur, 'PDB')

if __name__ == "__main__":
    pdb_files_compteur = fichier_pdb()
    pdb_files = pdb_files_compteur[0]
    compteur = pdb_files_compteur[1]
    #pairwaise(pdb_files)
    #merge_files()
    all_veres_all()
    compteur_t(list_processing())
    #list_processing()