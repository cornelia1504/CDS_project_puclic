# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Connection to CAZy database"""
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import os
import mysql.connector

def connection_db():
    """Connection to CAZy database
    Sets a cursor
    """
    my_db = mysql.connector.connect(host="10.1.22.207",
                                    user="glyco",
                                    password="Horror3",
                                    database="pdb")
    my_cursor = my_db.cursor()

    # Exécuter une commande SQL
    my_cursor.execute("SELECT * FROM pdb_info WHERE pdb_code = '6LFZ'")

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
                                    database="pdb")
    my_cursor = my_db.cursor()

    # Exécuter une commande SQL
    my_cursor.execute("SELECT resolution FROM pdb_info WHERE pdb_code = '6LFZ'")

    # Récupérer les résultats de la commande SQL
    result = my_cursor.fetchall()
    print('res2= ',result)
    # Fermer la connexion à la base de données
    my_db.close()

if __name__ == '__main__' :
    connection_db()
    requete()