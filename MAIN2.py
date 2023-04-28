"""Main script"""

import os
import retrieve_pdb as rpdb
import alphaFold as af
import pre_traitement_pdb as ppdb
##################################################################
def famille():
    global family_names
    family_names = input('Enter the family names separate by a comma :').split(',')

##################################################################

##################################################################
if __name__ == "__main__":
    """definir famille"""
    famille()