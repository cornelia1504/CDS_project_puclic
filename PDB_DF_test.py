from biopandas.pdb import PandasPdb

pdb_file = '/home/guest/Documents/Cornelia/cds_project/GH62/PDB_GH62/modeles_alph5/A2QFV9_alph.pdb'
ppdb = PandasPdb()
ppdb.read_pdb(pdb_file)
df_pdb = ppdb.df['ATOM']
print(df_pdb)
###################
'''Select regions with pLDDT score of 50 or above'''
results_df = df_pdb[df_pdb['b_factor'].astype(float) >= 70]

'''Write novel pdb file'''
fh_pdb = open('A2QFV9_alph_clean70.pdb', 'w')
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
###################"
#f = ppdb.df['ATOM'].head()
#print(f)