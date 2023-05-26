"""Ce programme a pour but de nettoyer les PDB
    afin qu'ils soient traitables par le logiciel maxcluster"""

from Bio.PDB import *
import os
def report_pdb(pdb_accessions_list,family):
    """function to retrieve pdb files of a list of accessions"""
    print('*********** report_pdb ***********')
    fam_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}'
    if not os.path.exists(fam_folder):
        os.mkdir(fam_folder)
    output_folder = f'/home/guest/Documents/Cornelia/cds_project/{family}/PDB'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    for accession in pdb_accessions_list :
        output_file = os.path.join(output_folder, f"{accession}.pdb")

        os.system(f'wget -O {output_file} https://files.rcsb.org/download/{accession}.pdb')
        if not os.path.exists(output_file):
            os.mkdir(output_file)
    compteur = 0
    for i in pdb_accessions_list:
        compteur += 1
    pdb_files = os.listdir(output_folder)
    nb_files = len(pdb_files)
    print(f'{nb_files} fichiers PDB téléchargés sur {compteur} accessions')

def pdb_cleaner(family):
    print('*********** pdb_cleaner ***********')
    #for family in family_names:
    pdb_files = os.listdir('/home/guest/Documents/Cornelia/cds_project/'
                            +family+'/PDB')
    print(pdb_files)
    for pdb_file in pdb_files:
        parser = PDBParser()
        s = parser.get_structure(pdb_file, '/home/guest/Documents/Cornelia/cds_project/'
                                 +family+'/PDB/'
                                 +pdb_file)
        io = PDBIO()
        class NotDisordered(Select):
            def accept_atom(self, atom):
                return not atom.is_disordered() or atom.get_altloc() == "A"

        io = PDBIO()
        io.set_structure(s)

        output_folder = f'/home/guest/Documents/Cornelia/cds_project/' \
                        f'{family}/ordered_pdb_file'
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        io.save(output_folder+"/"+pdb_file, select=NotDisordered())

def split_pdb(family):
    print('*********** split_pdb ***********')
    pdb_files = []
    #for family in family_names:
    pdb_files_name = os.listdir('/home/guest/Documents/Cornelia/cds_project/'
                                + family + '/ordered_pdb_file')
    print(pdb_files_name)
    directory = '/home/guest/Documents/Cornelia/cds_project/' \
                + family + '/ordered_pdb_file/'
    for pdb_file in pdb_files_name:
        pdb_files.append(f'{directory}{pdb_file}')

    output_clean = f'/home/guest/Documents/Cornelia/cds_project/' \
                   f'{family}/clean_pdb_A/'
    if not os.path.exists(output_clean):
        os.mkdir(output_clean)

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
            if chain == 'A':
                chain_file = os.path.splitext(pdb_file)[0] + f'_{chain}.pdb'
                code_fichier = os.path.basename(pdb_file)[:4]
                chain_file = f'{output_clean}' + f'{code_fichier}_{chain}.pdb'
                with open(f'{chain_file}', 'w') as f:
                    for line in lines:
                        if (line.startswith('ATOM') or line.startswith('HETATM')) and line[21] == chain:
                            f.write(line)

    #####################################################################################################
