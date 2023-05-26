# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on mai 2023

@author: Mamitiana Mahitasoa
"""
"""Main script"""
import time
import retrieve_pdb as rpdb
import retrieve_db_info as db
import clustering as cl
import uniprot_id_mapping as map
import alphafold as alf
import matrix_tree as mx
import maxCluster as max
import os
#import pre_traitement_pdb as ppdb
##################################################################
def famille():
    global family_names
    family_names = input('Enter the family names separate by a comma :').split(',')
    return family_names

##################################################################
folder = '/home/guest/Documents/Cornelia/cds_project'
if not os.path.exists(folder):
    os.makedirs(folder)
def download_pdb(family) :
    pdb_info_db = db.info_parser_pdb(family)
    pdb_accessions_list = pdb_info_db[0]
    rpdb.report_pdb(pdb_accessions_list,family)

def clustering(family):
    cl.Pisces(family)

def order_pdb(family) :
    rpdb.pdb_cleaner(family) #pdb_cleaner(family_names)
    rpdb.split_pdb(family)

def alphafold(family):
    family = input('famille : ')
    print('**')
    alf.search_accession_alf(family)
    alf.retrieve_alf(family)

#/home/guest/Documents/Cornelia/cds_project/GH62
##################################################################

if __name__ == "__main__":
    """definir famille"""
    #family = famille().__str__()
    start = time.time()
    family = input('famille : ')
    """importer les PDB"""
    download_pdb(family)
    """traiter les pdb"""
    rpdb.pdb_cleaner(family)  # pdb_cleaner(family_names)
    rpdb.split_pdb(family)
    """clustering"""
    cl.Pisces(family)
    """alphafold"""
    map.search_accession_alf_50(family)
    alf.retrieve_alf(family)
    alf.clean_alf(family)
    """maxcluster"""
    max.merge_files(family)
    max.all_vs_all(family)
    """matrix"""
    mx.extract_result(family)
    mx.extract_scores(family)
    mx.tableau_score(family)
    mx.extract_pd_name(family)
    mx.built_matrix_max(family)
    """fastME"""
    mx.fastme(family)
    end = time.time()
    print('**')
    temps = (end-start)/60
    print('\n Analyse faite en ', temps, f'min pour la famille : {family}')