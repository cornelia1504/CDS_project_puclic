import retrieve_db_info as db
import pandas as pd

def Pisces(family):
    """function to retrieve representatives pdb"""
    url = "http://dunbrack.fccc.edu/pisces/download/"
    fichier = "cullpdb_pc50.0_res0.0-5.0_noBrks_len40-10000_R1.0_Xray+Nmr+EM_d2023_05_01_chains31530"
    pdb_info_db = db.info_parser_pdb(family)
    pdb_ids = pdb_info_db[1]
    with open(fichier, 'r') as f:
        read_file = pd.read_table(f, sep='\s+')
        # Extraction des numéros d'accession
        accession_numbers = read_file['PDBchain'].tolist()
        #print(accession_numbers)
    representants = [j[0:4] for j in pdb_ids if j in accession_numbers]
    print('Representants = ', representants)
    print(len(representants))
    representant_file = f'/home/guest/Documents/Cornelia/cds_project/{family}/maxcluster/'
    with open(representant_file + "representant.txt", "w") as output_file:
        output_file.write('Les structures représentatives pour cette famille sont : ' + str(representants))
    return representants
#Pisces('GH128')