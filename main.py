"""Main script"""

import retrieve_pdb as rpdb
import alphaFold as af
#import pre_traitement_pdb as ppdb
##################################################################
def famille():
    global family_names
    family_names = input('Enter the family names separate by a comma :').split(',')
    return family_names

##################################################################
def order_pdb():
    print('Traitement des fichiers PDB ..............................')
    import pre_traitement_pdb as ppdb
    ppdb()

##################################################################
if __name__ == "__main__":
    """definir famille"""
    cazy_family = famille()
    """importer les PDB"""
    pdb_path = rpdb.family(cazy_family)
    list_path = pdb_path[0]
    output_folder = pdb_path[1]
    rpdb.ids_for_rcsb(cazy_family,list_path)
    rpdb.compte_ids()
    rpdb.report_pdb(output_folder)
    rpdb.compte_pdb_files(output_folder)
    """importer les modeles alphafold"""
    af.ids_for_alph()
    af.compte_ids()
    af.download_pdb()
    af.compte_pdb_files()
    """traiter les fichiers PDB"""
    order_pdb()
