"""Main script to retrieve pdb files for a given list of acccession """

import os

#############
####PATH#####
#############
#family_names = input('RCSB Enter the family names separate by a comma :').split(',')
list_paths = {}
def family(family_names):
    print(family_names)
    for family in family_names:
        list_path = '/home/guest/Documents/Cornelia/cds_project/'+family.strip()+'/'+family.strip()+'.list'
        list_paths[family] = list_path
        print(list_path)
    output_folder = '/home/guest/Documents/Cornelia/cds_project/'+family.strip()+'/PDB_'+family.strip()+'/pdb_rcsb'
    return list_path, output_folder

##############
##FUNCTIONS###
##############

#/home/guest/Documents/Cornelia/cds_project/GH62/id_mapping/id_map_GH62_unKB.xlsx
accessions = []
def ids_for_rcsb(family_names, list_path):
    for family in family_names:
        file_path = list_path
    with open(file_path, 'r') as f:
        accession = f.readlines()
        for line in accession:
            accessions.append(line.strip())
    print(accessions)

def compte_ids():
    global compteur
    compteur= 0
    for i in accessions:
        compteur += 1
    print('nombre de PDB à télécharger: ',compteur)

######################################################################################
def report_pdb(output_folder):
    """function to retrieve pdb files of a list of IDS"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for accession in accessions :
        output_file = os.path.join(output_folder, f"{accession}.pdb")
        os.system(f'wget -O {output_file} https://files.rcsb.org/download/{accession}.pdb')
        #https://files.rcsb.org/download/4PVI.pdb
######################################################################################

def compte_pdb_files(output_folder):
    directory = output_folder
    pdb_files = os.listdir(directory)

    nb_files = len(pdb_files)
    print(f'{nb_files} fichiers PDB téléchargés sur {compteur} accessions')

if __name__ == "__main__":
    ids_for_rcsb()
    compte_ids()
    report_pdb()
    compte_pdb_files()