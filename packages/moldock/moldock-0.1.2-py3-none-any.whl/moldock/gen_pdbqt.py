from rdkit import Chem
from moldock.preparation_for_docking import mk_prepare_ligand

# for mol in Chem.SDMolSupplier('/home/pavel/Teaching/UPOL/ADD/2023/challedge/jak3/final_data/blind2_protonated_full.sdf',
#                               removeHs=False):
#     pdbqt = mk_prepare_ligand(mol)
#     mol_name = mol.GetProp('_Name')
#     with open('/home/pavel/Teaching/UPOL/ADD/2023/challedge/jak3/final_data/blind2_protonated_full_pdbqt/' + mol_name + '.pdbqt', 'wt') as f:
#         f.write(pdbqt)

for mol in Chem.SDMolSupplier('/home/pavel/Teaching/UPOL/ADD/2023/challedge/jak3/final_data/train_protonated_full2.sdf',
                              removeHs=False):
    pdbqt = mk_prepare_ligand(mol)
    mol_name = mol.GetProp('_Name')
    with open('/home/pavel/Teaching/UPOL/ADD/2023/challedge/jak3/final_data/train_pdbqt/' + mol_name + '.pdbqt', 'wt') as f:
        f.write(pdbqt)
