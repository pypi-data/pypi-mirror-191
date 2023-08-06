import os

env_name = 'vina'
input_files = ['/mnt/proj2/open-23-32/cache/denovo/combine_4weeks/selection1.smi']
protein_files = ['/home/minibaevag/proteins/ready/6dlo.pdbqt', '/home/minibaevag/proteins/ready/run0.pdbqt']
# the length of config_files should be equal to the length of protein_files,
# if identical configs are used for different proteins just duplicate them
config_files = ['/home/minibaevag/proteins/ready/config_big.txt'] * 2
scorings = [('rescore', 'default'), ('none', 'vinardo')]
output_dir = '/home/pavel/python/docking-scripts/test'  # dir where all db will be stored

pbs_jobs_dir = os.path.join(output_dir, 'jobs')  # dir where pbs scripts will be stored
os.makedirs(pbs_jobs_dir, exist_ok=True)

# GNINA
for input_file in input_files:
    for protein_file, config_file in zip(protein_files, config_files):
        for cnn_scoring, scoring in scorings:
            prot = os.path.basename(os.path.splitext(protein_file)[0])
            conf = os.path.basename(os.path.splitext(config_file)[0])
            input = os.path.basename(os.path.splitext(input_file)[0])
            db_basename = f'{input}_{prot}_{conf}_{cnn_scoring}_{scoring}'
            output_db = os.path.join(output_dir, f'{db_basename}.db')
            with open(os.path.join(pbs_jobs_dir, f'{db_basename}.pbs'), 'wt') as f:
                f.write(f"""#!/bin/bash
#PBS -l select=1
#PBS -q qexp
#PBS -A OPEN-23-32
#PBS -k oe

source activate {env_name}

gnina_dock \ 
-i {input_file} \ 
-o {output_db} \ 
-p {protein_file} \ 
-s {config_file} \ 
--cnn_scoring {cnn_scoring} \ 
--cnn dense_ensemble \ 
--num_modes 9 \ 
--scoring {scoring} \ 
--exhaustiveness 32 \ 
--seed 120 \ 
--install_dir /home/minibaevag/ \ 
--ncpu 128
""")


# VINA
for input_file in input_files:
    for protein_file, config_file in zip(protein_files, config_files):
        prot = os.path.basename(os.path.splitext(protein_file)[0])
        conf = os.path.basename(os.path.splitext(config_file)[0])
        input = os.path.basename(os.path.splitext(input_file)[0])
        db_basename = f'{input}_{prot}_{conf}_vina'
        output_db = os.path.join(output_dir, f'{db_basename}.db')
        with open(os.path.join(pbs_jobs_dir, f'{db_basename}.pbs'), 'wt') as f:
            f.write(f"""#!/bin/bash
#PBS -l select=1
#PBS -q qexp
#PBS -A OPEN-23-32
#PBS -k oe

source activate {env_name}

vina_dock \ 
-i {input_file} \ 
-o {output_db} \ 
-p {protein_file} \ 
-s {config_file} \ 
--sdf \ 
--exhaustiveness 32 \ 
--seed 120 \ 
--ncpu 128
""")
