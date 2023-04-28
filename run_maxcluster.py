
import os
import subprocess

maxcluster_path = "/home/guest/Documents/Cornelia/cds_project/MAXCLUSTER/maxcluster64bit" # Chemin d'accès à MaxCluster
config_file = "maxcluster.cfg" # Chemin d'accès au fichier de configuration
pdb_directory = "/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/ordered_pdb" # Répertoire contenant les fichiers PDB

# Récupérez la liste des fichiers PDB
pdb_files = os.listdir(pdb_directory)

# Exécutez MaxCluster pour chaque paire de fichiers PDB
for i, pdb1 in enumerate(pdb_files):
    for j, pdb2 in enumerate(pdb_files):
        if i < j:
            # Exécutez MaxCluster avec les fichiers PDB
            subprocess.run([maxcluster_path, "-c", config_file, pdb1, pdb2])