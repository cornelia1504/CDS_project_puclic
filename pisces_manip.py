""" This is the main script to get the pdb files for a given list of IDs
This program requires using module_cif_pdb.py to convert cif format files to pdb
"""
import os
import pandas as pd

#############
####PATH#####
#############
family_names = input('Enter the family names separate by a comma :').split(',')
pdb_list_paths = {}
print(family_names)
for family in family_names:
    pdb_list_path = '/home/guest/Documents/Cornelia/cds_project/script/' + family.strip() + '.raw'
    pdb_list_paths[family] = pdb_list_path
    print(pdb_list_path)
output_folder = '/home/guest/Documents/Cornelia/cds_project/script/' + family.strip() + '_pisces_result/'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

##############
##FUNCTIONS###
##############
def check():
    print(os.system(f'head {pdb_list_path}'))
    print(os.system(f'head {output_folder}{family}.list'))
def chain_extraction():
    """extraction of the chain A/B in the pdb code"""
    os.system(f'cat {pdb_list_path} | cut -c1-4 > {output_folder}{family}.list')

def pisces(): #../Pisces/files/cullpdb_pc50.0_res0.0-5.0_noBrks_len40-10000_R1.0_Xray+Nmr+EM_d2023_03_11_chains31265
    """ """
    pisces_50 = '../Pisces/files/cullpdb_pc50.0_res0.0-5.0_noBrks_len40-10000_R1.0_Xray+Nmr+EM_d2023_03_11_chains31265'
    #create request for all pdb code in the clear list
   ## os.system(f"cat {output_folder}{family}.list | awk '{{print \"grep @^\" $1 \"@ {pisces_50} >> grep_res.txt}}' | sed \"s/@/'/g\" >> commandes_grep.txt")
    ##os.system(f"cat {output_folder}{family}.list | awk '{{print \"grep @^\" $1 \"@ {{pisces_50}} >> test.sh\" }}' | sed 's/@/\"/g'")

    with open('commandes_grep.txt', 'r') as com:
        commandes = com.readlines()
        print(commandes)
        for lines in commandes:
            os.system(f'{lines}')
        os.system('more grep_res.txt')

############################################################################################################################################

def report_cif():
    """function to retrieve cif files of a list of IDS"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(pdb_list_path, 'r') as f:
        contenu = f.read()
        pdb_list = contenu.split()

    for pdb in pdb_list:
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
    chain_extraction()
    check()
    pisces()