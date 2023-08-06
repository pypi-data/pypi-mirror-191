#Defining he element's table
atom=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe']
z=[x for x in range(1,55,1)]
Atom=pd.DataFrame(atom,columns=['Atom'])
Z=pd.DataFrame(z,columns=['Z'])
tab=pd.concat([Atom,Z],axis=1)

#Creating MAOC
def mol_MAOC(path, basis_set='pcseg-0',charge=0,spin=0):
    from pyscf import scf,gto,lo
    import glob
    import numpy as np
    import pandas as pd
    from natsort import natsorted
    rep_stored=[]
    for file in natsorted(glob.glob(path)):
        q=pd.DataFrame([x.split() for x in open(file).readlines()[2:]])[0]
        atom_types=[x for x in pd.DataFrame(q)[0] if x is not None]
        atom_charge=[]
        for g in atom_types:
            atom_charge.append(tab['Z'][tab.index[tab['Atom'] == g].tolist()[0]])
        mol1 = gto.Mole()
        mol1.atom = file
        mol1.charge=charge
        mol1.spin=abs((mol1.nelectron) % 2)
        p=list(set(atom_charge))
        atom_1=[]
        for t in list(p):
            atom_1.append(tab['Atom'][tab.index[tab['Z'] == t].tolist()[0]])
        atom_1=[x for x in atom_1 if x is not None]
        times=atom_charge.count(max(atom_charge))
        typ=tab['Atom'][tab.index[tab['Z'] == max(atom_charge)].tolist()[0]]
        if times==1:
            atom_1.remove(typ)
            dic={x:basis_set for x in atom_1}
            dic[str(typ)]=gto.basis.load(basis_set, tab['Atom'][tab.index[tab['Z'] == (max(atom_charge)-mol1.charge)].tolist()[0]])
        else:
            dic={x:basis_set for x in atom_1}
            dic[str(typ)+':0']=gto.basis.load(basis_set, tab['Atom'][tab.index[tab['Z'] == (max(atom_charge)-mol1.charge)].tolist()[0]])
        atom_types=[]
        mol1.basis=dic
        mol1.build()
        core=lo.orth_ao(mol1)
        core=pd.DataFrame(core)
        for col in core:
            core[col] = core[col].sort_values(ignore_index=True,ascending=False)
        sqr_core = core.sort_values(by =0, axis=1,ascending=False)
        sqr_core=abs(pd.DataFrame(sqr_core)).round(4)
        rep_stored.append(sqr_core.to_numpy().flatten())
    return rep_stored
