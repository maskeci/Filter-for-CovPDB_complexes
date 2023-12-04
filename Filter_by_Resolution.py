import os, shutil
from os import listdir

# Find and list all complexes in folder that in samae location with this script
complex_folder = "CovPDB_complexes"
cwd = os.path.join(os.getcwd(), complex_folder)

complexes = [f for f in listdir(cwd)]

# Create new folder in current directory
name_newfolder = "Resolution_2.5"
newfolder = os.path.join(os.getcwd(), name_newfolder)

if not os.path.exists(newfolder):
    os.makedirs(newfolder)

# Seaching and filtering
count = 0
for protein in complexes: # All index in "complexes" list are also name of the folder and name of the pdb file
    
    protein_folder = os.path.join(cwd, protein) # Directory of parent folder
    pdb_file = os.path.join(protein_folder, f'{protein}.pdb') # Directory of pdb file
    
    with open(pdb_file, 'r') as pdb:
        for line in pdb:
            if 'REMARK   2 RESOLUTION' in line: # Finds resolution line in pdb
                line = line.split()      
                try:
                    resolution = float(line[3])     
                    if resolution >= 2.5:
                        destination_folder = os.path.join(newfolder, protein)
                        shutil.copytree(protein_folder, destination_folder)
                        print(f'{protein} with the resolution of {resolution} is copied to {destination_folder} ') 
                        count += 1
                    break  
                except:
                    #print(f'No resolution data of {protein}')
                    pass
   
print(f'>>>> {count} folder filtered <<<<')
