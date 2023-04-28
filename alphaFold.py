"""Main script to retrieve pdb files for a given list of acccession """

import os
from biopandas.pdb import PandasPdb

#/home/guest/Documents/Cornelia/cds_project/GH62/id_mapping/id_map_GH62_unKB.xlsx
accessions = []
accession2 = []
def ids_for_alph():
    file_path = 'accession_numbers.txt'
    with open(file_path, 'r') as f:
        accession = f.readlines()
        accession2 =f.readlines()
        for line in accession:
            if len(line.strip())==6:
                accessions.append(line.strip())
            elif len(line.strip())!=6:
                accession2.append(line.strip())
    print(accessions)
    print(accession2)

def compte_ids():
    global compteur
    compteur= 0
    for i in accessions:
        compteur += 1
    print('nombre d accessions avec un modèle Alphafold disponible : ',compteur)
    compteur2= 0
    for i in accession2:
        compteur2 += 1
    print('nombre d accessions avec un modèle Alphafold non disponible : ',compteur2)

def download_pdb() :
    """function to retrieve alphafold modeles pdb files of a list of accession"""
    global output_folder
    output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/modeles_alph5'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for accession in accessions:
        output_file = os.path.join(output_folder, f"{accession}_alph.pdb")
        os.system(f'wget -O {output_file} https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v4.pdb')
        #https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-model_v4.pdb

def clean_alf():
    models_folder = os.listdir('/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/modeles_alph5')
    print(models_folder)
    models = []
    for i in models_folder:
        models.append(f'/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/modeles_alph5/{i}')
    for pdb in models:
        pdb_file = pdb
        print(pdb_file)
        pdb_accession = os.path.basename(pdb_file)
        pdb_accession = pdb_accession[0:10]
        print(pdb_accession)
        ppdb = PandasPdb()
        ppdb.read_pdb(pdb_file)
        df_pdb = ppdb.df['ATOM']
        print(df_pdb)
        ###################
        '''Select regions with pLDDT score of 50 or above'''
        results_df = df_pdb[df_pdb['b_factor'].astype(float) >= 70]

        '''Write novel pdb file'''
        output_folder = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/clean_pdb_alph70'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        fh_pdb = open(f'{output_folder}/{pdb_accession}_C70.pdb', 'w')
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
def compte_pdb_files():
    directory = output_folder
    pdb_files = os.listdir(directory)

    nb_files = len(pdb_files)
    print(f'{nb_files} modèles télécharger sur {compteur} accessions pdb')

if __name__ == "__main__":
    ids_for_alph()
    compte_ids()
    # download_pdb()
    # compte_pdb_files()
    #clean_alf()
