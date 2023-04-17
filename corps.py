""" This is the main script to get the pdb files for a given list of IDs
This program requires using module_cif_pdb.py to convert cif format files to pdb
"""
import os

#############
####PATH#####
#############
family_names = input('Enter the family names separate by a comma :').split(',')
pdb_list_paths = {}
print(family_names)
for family in family_names:
    pdb_list_path = '/home/guest/Documents/Cornelia/cds_project/script/'+family.strip()+'.list'
    pdb_list_paths[family] = pdb_list_path
    print(pdb_list_path)
output_folder = input('Enter the path of the output folder: ')

##############
##FUNCTIONS###
##############
def report_cif():
    """function to retrieve cif files of a list of IDS"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(pdb_list_path, 'r') as f:
        contenu = f.read()
        pdb_list = contenu.split()

    for pdb in pdb_list :
        output_file = os.path.join(output_folder, f"{pdb}.cif")
        os.system(f'wget -O {output_file} https://files.rcsb.org/download/{pdb}.cif')

def cif_pdb():
    """function to convert cif files to pdb files"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cif_list_path = output_folder
    cif_files = os.listdir(cif_list_path)

    for cif in cif_files:
        input_file = os.path.join(cif_list_path, cif)
        output_file = os.path.join(output_folder, f"{cif}.pdb")
        os.system(f'python3 module_cif_pdb.py {input_file} {output_file}')

if __name__ == "__main__":
    report_cif()
    cif_pdb()
