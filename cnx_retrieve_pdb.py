#Pub_from_PDB crée un fichier HTML des PDB des entrées CAZy non - caractérisées pour lesquelles une publi apparait dans le.cif(pas blacklistée non plus) pour connection

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 10:22:44 2021

@author: Suzan Dogan

     Search for new functions through the publications/references of PDB
proteins

"""

#######################
##     VARIABLES     ##
#######################
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import os
import mysql.connector


# If not installed:
# os.system('pip3 install mysql-connector-python')

#################
##  FUNCTIONS  ##
#################
def connection_db():
    """Connection to CAZy database
    Sets a cursor
    """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="cazy_7")
    my_cursor = my_db.cursor()
    return my_db, my_cursor


def id_2_dl(dico, data_path):
    os.system('rm ' + data_path + '/*.cif;')
    os.system('mkdir ' + data_path)
    for pdb in dico:
        os.system('wget -P ' + data_path
                  + 'https: // files.rcsb.org / download / '+pdb+'.cif')

def pdb_publi(dico):
    """ Extract the PubMed id of the 'Primary Citation' of PDB's CIF files
    'Primary Citation' which means not all the secondary references

    If there is no PMid, then extract the doi
    if no doi then... go see yourself

    Return: 3 dictionaries
        unreleased -> dict with the PDB ids of unreleased protein structure
        publi -> dict with the 'Primary Citation' (doi or PMID) as key
and the PDB ids as value
        new_from_obs -> dict with the new PDB ids (key) of the obsolete
PDB ids from CAZy (value)
                        can be used for a second run of pdb_publi
function with new_from_obs dictionary
    """
    path_result = input('Enter the path to the directory where to store the results : ')
    # set a directory and download pdb files
    data_path = path_result + 'data_pdb/'
    id_2_dl(dico, data_path)

    unreleased = {}
    publi = {}
    new_from_obs = {}
    for PDBID in dico:
        L = []
        try:
            cif_dict = MMCIF2Dict(data_path + PDBID + ".cif")
        except:
            unreleased.update({PDBID: dico[PDBID]})
        else:
            cif_dict = MMCIF2Dict(data_path + PDBID + ".cif")
            for state in cif_dict["_pdbx_database_status.status_code"]:
                if state == 'OBS':
                    for new_PDB in cif_dict["_pdbx_database_PDB_obs_spr.pdb_id"]:
                        if new_PDB not in dico:
                            if new_PDB not in new_from_obs:
                                new_from_obs[new_PDB] = dict()
                            new_from_obs[new_PDB].update({PDBID: True})
                else:
                    citation = cif_dict["_citation.journal_abbrev"]
                    PubMeds = cif_dict["_citation.pdbx_database_id_PubMed"]
                    keyword = cif_dict["_struct_keywords.pdbx_keywords"]
                    DOI = cif_dict['_citation.pdbx_database_id_DOI']
                    link = "/" + PDBID
                    if citation[0].lower() != 'to be published':
                        if 'UNKNOWN FUNCTION' not in keyword:
                        # L = sorted(dico[PDBID], key=lambda key: dico[PDBID][key])
                            pubmed = PubMeds[0]
                            if pubmed != '?':
                                if pubmed not in publi:
                                    publi[pubmed] = dict()
                                for cazy in dico[PDBID]:
                                    if cazy not in publi[pubmed]:
                                        publi[pubmed][cazy] = dict()
                                        publi[pubmed][cazy].update({PDBID: True})
                                        # publi[pubmed].update({PDBID:L})
                            else:
                                doi = DOI[0]
                                if doi != '?':
                                    if doi not in publi:
                                        publi[doi] = dict()
                                    for cazy in dico[PDBID]:
                                        if cazy not in publi[doi]:
                                            publi[doi][cazy] = dict()
                                            publi[doi][cazy].update({PDBID: True})
                                            return unreleased, publi, new_from_obs
# else:
#   if link not in publi:
#       publi[link] = dict()
#    for cazy in dico[PDBID]:
#        if cazy not in publi[link]:
# publi[link][cazy]=dict()
# publi[link][cazy].update({PDBID:True})
# #publi[link].update({PDBID:L})


################
####  MAIN  ####
################

# Retrieve uncharacterized CAZymes (Nico : not limited to enzymes
# anymore by removing ->  WHERE class='enzyme')
my_db, my_cursor = connection_db()
cazy_PDB , origin_PDB = from_db_2_dico("""
    SELECT entry_id,
        IF(db_name='pdb' AND LOCATE('_',db_acc)!=0, SUBSTR(db_acc,1,LOCATE('_',db_acc)-1),
            IF((db_name='ncbi' OR db_name='uniprot') AND LOCATE('.',db_acc)!=0,
                SUBSTR(db_acc,1,LOCATE('.',db_acc)-1),db_acc)),
        db_name
    FROM annotation INNER JOIN entry USING(entry_id)
    WHERE entry_id NOT IN (SELECT entry_id FROM entry_func INNER JOIN function USING(function_id))
    AND is_confidential='0'
    AND db_name='pdb'
    AND (db_acc IS NOT NULL OR db_acc != '');""", my_db, my_cursor)
my_db.close()



# Read CIF files, fetch publications and save them into TXT file
unreleased, publi, new_from_obs = pdb_publi(cazy_PDB)

# Read the blacklisted publications (not reporting a "true" function)
blackL={}
with open(path + "uniprot/PMID-blacklist.txt") as f:
    for line in f:
        line=line.rstrip()
        if line != "":
            blackL[line]=True

# Write result to file
#dico_2_texte(path_result+'PDB_pub/', publi, 'PDB_Publications.txt')
os.system('mkdir -p '+ path_result+'PDB_pub/')
with open(path_result + 'PDB_pub/PDB_Publications.html', 'w') as f:
    f.write('<html><body><table border="1">\n')
    for art in publi:
        if art not in blackL:
            f.write('<tr><td rowspan="'+str(len(publi[art]))+'"><a href="')
            if "/" in art:
                if "." in art:
                    f.write('https://doi.org/'+str(art)+'">'+str(art))
                else:
                    f.write('https://www.rcsb.org/structure'+str(art)+'">'+str(art[1:]))
            else:
                f.write('https://pubmed.ncbi.nlm.nih.gov/'+str(art)+'">'+str(art))
            f.write('</a></td>\n')
            cpt=0
            for cazy in publi[art]:
                if cpt > 0 :
                    f.write('</tr>\n<tr>')
                pdbs = ''
                for pdb in publi[art][cazy]:
                    pdbs =  pdb + ", " + pdbs
                f.write('<td><a href="http://10.1.22.212/privatesite/cazy_views.cgi?intype=entry&searchterm='
                        + str(cazy) + '">' + str(cazy) + '</a></td><td>' + str(pdbs[0:-2]) + '</td>')
                cpt = cpt + 1
            f.write('</tr>\n')
    f.write('</table></body></html>\n')

if len(new_from_obs) > 0 :
    print("New PDB, replaced Obsoletes")
    for n in new_from_obs:
        print(n + ' replaced obsolete:')
        for o in new_from_obs[n]:
            print(o)
        print('')

# Second run with the obsolete accessions
# unreleased2, publi2, new_from_obs2 = pdb_publi(new_from_obs)
# dico_2_texte(path_result+'PDB_publications/', publi2, 'PDB_Publications2.txt')
