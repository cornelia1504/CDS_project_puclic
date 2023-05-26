# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Created on mai 2023

@author: Mamitiana Mahitasoa

Connection to CAZy database"""

import mysql.connector
import pandas as pd
from inscriptis import get_text
import re
import time

#family = input ('family : ')
def connection_db():
    """Connection to CAZy database
    Sets a cursor
    """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="web_dataset")
    my_cursor = my_db.cursor()

    # Exécuter une commande SQL
    my_cursor.execute("SELECT pdb, uniprot FROM `web_visa` WHERE `family`='GH62' AND `pdb` <> '&nbsp;'; ")

    # Récupérer les résultats de la commande SQL
    result = my_cursor.fetchall()
    print('res1= ',result)
    # Fermer la connexion à la base de données
    my_db.close()

def requete(family):
    """Connection to CAZy database
    Sets a cursor
    """
    print('*********** requete ***********')

    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="web_dataset")
    my_cursor = my_db.cursor()

    # Exécuter une commande SQL
    my_cursor.execute(f"SELECT pdb, ncbi, uniprot FROM `web_visa` WHERE `family`='{family}' AND `pdb` <> '&nbsp;'; ")
    # Récupérer les résultats de la commande SQL
    result = my_cursor.fetchall()
    #print('pdb_uniprot = ',result)

    b = my_cursor.execute(f"SELECT pdb FROM `web_visa` WHERE `family`='{family}' AND `pdb` <> '&nbsp;'; ")
    # Récupérer les résultats de la commande SQL
    result_pdb = my_cursor.fetchall()
    #print('pdb = ', result_pdb)

    c = my_cursor.execute(f"SELECT uniprot FROM `web_visa` WHERE `family`='{family}' AND `pdb` <> '&nbsp;'; ")
    # Récupérer les résultats de la commande SQL
    result_uniprot_link = my_cursor.fetchall()
    #print('uniprot_link= ',result_uniprot_link)

    c = my_cursor.execute(f"SELECT ncbi FROM `web_visa` WHERE `family`='{family}' AND `pdb` <> '&nbsp;'; ")
    # Récupérer les résultats de la commande SQL
    result_ncbi = my_cursor.fetchall()
    #print('ncbi= ', result_ncbi)

    d = my_cursor.execute(f"SELECT modularity FROM `web_cazomelist` WHERE `modularity` LIKE '%{family}%' ; ")
    # Récupérer les résultats de la commande SQL
    result_modularity = my_cursor.fetchall()
    #print('modularity= ', result_modularity)

    e = my_cursor.execute(f"SELECT visa FROM `web_visa` WHERE `family` LIKE '%{family}%' ; ")
    # Récupérer les résultats de la commande SQL
    result_visa = my_cursor.fetchall()


    # Fermer la connexion à la base de données
    my_db.close()
    return result_ncbi , result_pdb, result_modularity, result , result_visa

def accessions_ncbi(family):
    """Connection to CAZy database
    Sets a cursor
    """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="web_dataset")
    my_cursor = my_db.cursor()
    print('\n', '*********Récupérartion des accessions********** ', '\n')

    nb_visa = requete(family)
    visa_nb = nb_visa[4]
    print(visa_nb)

    accessions_cazy = []
    # Liste initiale
    # Expression régulière pour extraire les entiers
    pattern = r'\d+'

    # Liste des entiers extraits
    integers = [int(re.findall(pattern, str(item))[0]) for item in visa_nb]

    # Affichage des entiers
    print(integers)
    print(len(integers))
    for visa in integers[0:20]:
        my_cursor.execute(f"SELECT info FROM `web_entry` WHERE `visa` LIKE '%{visa}%' AND `title` = 'ncbi'; ")
        # Récupérer les résultats de la commande SQL
        results_visa = my_cursor.fetchall()
        print('***********' , visa, '***********',  results_visa)
        accessions_cazy.append(results_visa)
    print('###########################################')
    print(accessions_cazy)
    accessions = []
    for sublist in accessions_cazy:
        accession = sublist[0][0]
        accessions.append(accession)
    print(accessions)
    # Fermer la connexion à la base de données
    my_db.close()
    return accessions

def accession_ncbi_join(family):
    """Connection to CAZy database
       Sets a cursor
       """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="web_dataset")
    my_cursor = my_db.cursor()
    print('\n', '*********Récupérartion des accessions********** ', '\n')
    my_cursor.execute(
        "SELECT web_entry.info FROM web_entry INNER JOIN web_visa ON web_entry.visa = web_visa.visa "
        "WHERE web_visa.family LIKE %s AND web_visa.prot_name_brut NOT LIKE '%fragment%' AND web_entry.title = 'ncbi'",
        (f'%{family}%',))

    # Récupérer les résultats de la commande SQL
    results_visa = my_cursor.fetchall() #tuple des accessions
    #print('***********', 'Accessions', '***********', results_visa)
    accessions = [t[0] for t in results_visa]
    #print('###########################################')
    #print(accessions)
    print(len(accessions), 'accessions pour cette famille on été récupérés pour cette famille')
    # Fermer la connexion à la base de données
    my_db.close()

    return accessions


# print('###########################################')
# print(accessions_cazy)

def accessions_uniprot(family):
    """Connection to CAZy database
    Sets a cursor
    """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="web_dataset")
    my_cursor = my_db.cursor()
    nb_visa = requete(family)
    visa_nb = nb_visa[4]
    print(visa_nb)

    accessions_cazy = []
    # Liste initiale
    # Expression régulière pour extraire les entiers
    pattern = r'\d+'

    # Liste des entiers extraits
    integers = [int(re.findall(pattern, str(item))[0]) for item in visa_nb]

    # Affichage des entiers
    print(integers)

    for visa in integers[0:15]:
        accession_cazy_uniprot = []

        my_cursor.execute(f"SELECT info FROM `web_entry` WHERE `visa` LIKE '%{visa}%' AND `title` = 'uniprot'; ")
        # Récupérer les résultats de la commande SQL
        results_visa = my_cursor.fetchall()
        print('***********' , visa, '***********',  results_visa)
        accession_cazy_uniprot.append(results_visa)
    # print('###########################################')
    # print(accessions_cazy)
    accessions = []
    for sublist in accessions_cazy:
        accession = sublist[0][0]
        accessions.append(accession)
    print(accessions)
    # Fermer la connexion à la base de données
    my_db.close()
    return accessions

def dataframe(family):
    results = requete(family)
    result = results[3]
    result1 = results[0]
    result2 = results[2]
    result3 = results[1]

    #dataframes à partir des résultats de chaque requête SQL
    df = pd.DataFrame(result, columns=['ncbi','pdb', 'uniprot'])
    df1 = pd.DataFrame(result1, columns=['ncbi'])
    df2 = pd.DataFrame(result2, columns=['modularity'])
    df3 = pd.DataFrame(result3, columns=['pdb'])

    # Fusionner les dataframes en un seul dataframe
    df_merged = pd.concat([df1, df2, df3], axis=0)

    # Écrire le dataframe dans un fichier csv
    #df_merged.to_csv('result.csv', index=False)

    html = result3.__str__()
    text = get_text(html)
    return text
#################################################################

def info_parser_pdb(family):
    """expression régulière pour extraire les informations souhaitées"""
    print('*********** info_parser_pdb ***********')
    text = dataframe(family)
    data = text
    lines = data.split('\n')  # séparation par le caractère de saut de ligne
    tuples = [(line.strip(),) for line in lines if
              line]  # suppression des caractères de saut de ligne et création de tuples

    # boucle à travers la liste pour extraire les informations de chaque élément
    pdb_ids = []
    pdb_accessions = []
    for elements in tuples:
        string = elements.__str__()
        string = string[2:-4]  # enlever les parenthèses et les virgules non souhaitées
        elementss = string.split('), (')  # diviser la chaîne de caractères en une liste d'éléments
        #elements = [elem.strip() for elem in elements]  # supprimer les espaces avant et après chaque élément
        for i in elementss:
            if 'cryst' in i:
                continue
            pdb_id = re.search(r'\|([0-9A-Z]+)@', i).group(1)
            clean_chain = 'A'
            pdb_ids.append(f"{pdb_id}{clean_chain}")
            pdb_accessions.append(f"{pdb_id}")

    print("nombre d'accessions  pdb pour cette famille : ", len(pdb_ids))

    return pdb_accessions, pdb_ids

################################################################################
def organisme(family):
    """Connection to CAZy database
       Sets a cursor
       """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="web_dataset")
    my_cursor = my_db.cursor()
    print('\n', '*********Récupérartion des accessions & noms des organismes********** ', '\n')

    my_cursor.execute(f"SELECT web_entry.info, web_visa.org FROM web_entry INNER JOIN web_visa "
                      f"ON web_entry.visa = web_visa.visa "
                      f"WHERE web_visa.family LIKE '%{family}%' AND web_entry.title = 'ncbi'")

    # Récupérer les résultats de la commande SQL
    results_visa = my_cursor.fetchall() #tuple des accessions
    print('***********', 'Accessions', '***********', results_visa)
    accessions = [t[0] for t in results_visa]
    organisme = [t[1] for t in results_visa]
    dico_org = dict(zip(accessions, organisme))
    print('###########################################')
    print(accessions)
    print(len(accessions), 'accessions pour cette famille on été récupérés pour cette famille')
    print(organisme)
    print(len(organisme), 'organisme pour cette famille on été récupérés pour cette famille')
    print('dico-org ', dico_org)
    # Fermer la connexion à la base de données
    my_db.close()

    return accessions, dico_org, organisme
################################################################################
#16MAI
def organisme(family):
    """Connection to CAZy database
       Sets a cursor
       """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="web_dataset")
    my_cursor = my_db.cursor()
    print('\n', '*********Récupérartion des accessions & noms des organismes********** ', '\n')
    my_cursor.execute(f"SELECT web_entry.info, web_visa.org FROM web_entry INNER JOIN web_visa "
                      f"ON web_entry.visa = web_visa.visa "
                      f"WHERE web_visa.family LIKE '%{family}%' AND web_entry.title = 'ncbi'")

    # Récupérer les résultats de la commande SQL
    results_visa = my_cursor.fetchall() #tuple des accessions
    print('***********', 'Accessions', '***********', results_visa)
    accessions = [t[0] for t in results_visa]
    organisme = [t[1] for t in results_visa]
    dico_org = dict(zip(accessions, organisme))
    print('###########################################')
    print(accessions)
    print(len(accessions), 'accessions pour cette famille on été récupérés pour cette famille')
    print(organisme)
    print(len(organisme), 'organisme pour cette famille on été récupérés pour cette famille')
    print('dico-org ', dico_org)
    # Fermer la connexion à la base de données
    my_db.close()

    return accessions, dico_org, organisme
################################################################################

if __name__ == '__main__' :
    #connection_db()
    #requete(family)
    #dataframe()
    #info_parser_pdb(family)
    start = time.time()
    family = input('famille : ')
    accession_ncbi_join(family)
    #info_parser_pdb(family)
    #organisme(family)
    end = time.time()
    time = end - start
    print('Temps : ',time)
    #accessions_uniprot()