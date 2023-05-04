# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Connection to CAZy database"""
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import os
import mysql.connector
import pandas as pd
import urllib.request
from inscriptis import get_text
from html.parser import HTMLParser

family = input ('family : ')
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

def requete():
    """Connection to CAZy database
    Sets a cursor
    """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="web_dataset")
    my_cursor = my_db.cursor()

    # Exécuter une commande SQL
    my_cursor.execute(f"SELECT pdb, ncbi, uniprot FROM `web_visa` WHERE `family`='{family}' AND `pdb` <> '&nbsp;'; ")
    # Récupérer les résultats de la commande SQL
    result = my_cursor.fetchall()
    print('pdb_uniprot = ',result)

    b = my_cursor.execute(f"SELECT pdb FROM `web_visa` WHERE `family`='{family}' AND `pdb` <> '&nbsp;'; ")
    # Récupérer les résultats de la commande SQL
    result_pdb = my_cursor.fetchall()
    print('pdb = ', result_pdb)

    c = my_cursor.execute(f"SELECT uniprot FROM `web_visa` WHERE `family`='{family}' AND `pdb` <> '&nbsp;'; ")
    # Récupérer les résultats de la commande SQL
    result_uniprot_link = my_cursor.fetchall()
    print('uniprot_link= ',result_uniprot_link)

    c = my_cursor.execute(f"SELECT ncbi FROM `web_visa` WHERE `family`='{family}' AND `pdb` <> '&nbsp;'; ")
    # Récupérer les résultats de la commande SQL
    result_ncbi = my_cursor.fetchall()
    print('ncbi= ', result_ncbi)

    d = my_cursor.execute(f"SELECT modularity FROM `web_cazomelist` WHERE `modularity` LIKE '%{family}%' ; ")
    # Récupérer les résultats de la commande SQL
    result_modularity = my_cursor.fetchall()
    print('modularity= ', result_modularity)

    # Fermer la connexion à la base de données
    my_db.close()
    return result_ncbi , result_pdb, result_modularity, result

def dataframe():
    results = requete()
    result = results[3]
    result1 = results[0]
    result2 = results[2]
    result3 = results[1]

    #dataframes à partir des résultats de chaque requête SQL
    df = pd.DataFrame(result, columns=['ncbi','pdb', 'uniprot'])
    df1 = pd.DataFrame(result1, columns=['ncbi'])
    df2 = pd.DataFrame(result2, columns=['modularity'])
    df3 = pd.DataFrame(result3, columns=['pdb'])
    #df5 = pd.DataFrame(result5, columns=['uniprot'])
    print(df, df1, df2, df3)
    with open('dataframe_db_res.txt', 'w') as f:
        print(df, file=f)
    # Écrire les dataframes dans des fichiers csv séparés
    df1.to_csv('result1.csv', index=False)
    df2.to_csv('result2.csv', index=False)
    df3.to_csv('result3.csv', index=False)

    # Fusionner les dataframes en un seul dataframe
    df_merged = pd.concat([df1, df2, df3], axis=0)

    # Écrire le dataframe dans un fichier csv
    df_merged.to_csv('result.csv', index=False)

#################################################################
    html = result3.__str__()
    #html = '<font class="E"><a href="http://www.enzyme-databas...'
    text = get_text(html)
    print('**********************')
    print(text)

#################################################################


if __name__ == '__main__' :
    #connection_db()
    requete()
    dataframe()