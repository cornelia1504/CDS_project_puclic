from Bio.PDB import *
import os
from biopandas.pdb import PandasPdb

family_names = input('Enter the family names separate by a comma :').split(',')

for family in family_names:
    pdb_files = os.listdir('/home/guest/Documents/Cornelia/cds_project/'+family+'/PDB_'+family+'/pdb_rcsb')
    print(pdb_files)
####################################################################################################
def download_pdb():
    ppdb = PandasPdb().fetch_pdb('3eiy')
####################################################################################################
for pdb_file in pdb_files:
    parser = PDBParser()
    s = parser.get_structure(pdb_file, "/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/pdb_rcsb/"+pdb_file)
    io = PDBIO()
    class NotDisordered(Select):
        def accept_atom(self, atom):
            return not atom.is_disordered() or atom.get_altloc() == "A"


    io = PDBIO()
    io.set_structure(s)
    output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb'

    io.save(output_folder+"/"+pdb_file, select=NotDisordered())
####################################################################################################
''' '''
print('\n', '********************************************', '\n')
print('traitement en cours..........')
print('\n', '********************************************', '\n')
# list_file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/testAllPDB.txt'
paths = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb/'
files = os.listdir('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb')
# files = os.listdir(paths)
list_pdb_paths = []
for file in files:
    list_paths = f'{paths}{file}'
    # print(list_paths)
    list_pdb_paths.append(list_paths)
# print(list_pdb_paths)
#ligne =[]
with open('list_file.txt', 'w') as l:
    l.write('\n'.join(list_pdb_paths))
with open('list_file.txt', 'r') as l:
    paths = l.readlines()
    for line in paths :
        print(line)
        pdb_file = line.strip()
        code_pdb = os.path.basename(pdb_file)
####################################################################################################
        import pandas as pd
        with open(pdb_file , 'r'):
            print(pdb_file)
            #usecols=[0,1,2,3,4,5,6,7,8,9,10,11]
        col_names = ['0','1','2','3','chain','5','6','7','8','9','10','11']
        df = pd.read_table(pdb_file, sep='\s+', header= None)
        print(df)
        df.columns = col_names
        print(df)
        ligne_index = df[df['chain'] != 'A'].index
        print('*************************************************')
        print(ligne_index)
        print('####################################################')
        df.drop(ligne_index, inplace=True)
        print('***********')
        print(df)
        print('***********')
        output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/clean_pdb_forMAXCLUSTER/'
        df.to_csv(f'{output_folder}{code_pdb}', header= False,sep= '\t',index= False)
        #output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb/'
        #with open(f'{output_folder}{code_pdb}_clean.pdb', 'w') as f:
            #f.write(df)
        #clean_pdb.save(output_folder + "/clean" + pdb_file)

####################################################################################################
#/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb
output_clean = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/clean_PDB/'
def split_pdb(pdb_file):
    pdb_files = []
    for family in family_names:
        pdb_files_name = os.listdir('/home/guest/Documents/Cornelia/cds_project/' + family + '/PDB_' + family + '/ordered_pdb')
        print(pdb_files_name)
        directory = '/home/guest/Documents/Cornelia/cds_project/' + family + '/PDB_' + family + '/ordered_pdb/'
        for pdb_file in pdb_files_name:
            pdb_files.append(f'{directory}{pdb_file}')
            #print(pdb_files)
    print('**********************************')
    print(pdb_files)
    for pdb_file in pdb_files:
        with open(pdb_file, 'r') as f:
            lines = f.readlines()

        chains = set()

        # Trouver toutes les chaînes présentes dans le fichier
        for line in lines:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                chain = line[21]
                chains.add(chain)

        # Écrire chaque chaîne dans un fichier séparé
        for chain in chains:
            chain_file = os.path.splitext(pdb_file)[0] + f'_{chain}.pdb'
            #code_fichier = os.path.splitext(pdb_file)[0]
            code_fichier = os.path.basename(pdb_file)[:4]
            print(code_fichier)
            chain_file = f'{output_clean}' + f'{code_fichier}_{chain}.pdb'
            print(chain_file)
            with open(f'{chain_file}', 'w') as f:
                for line in lines:
                    if (line.startswith('ATOM') or line.startswith('HETATM')) and line[21] == chain:
                        f.write(line)
#for pdb_file in pdb_files:
split_pdb(pdb_file)

#####################################################################################################
print('PDB traités avec succès !')
