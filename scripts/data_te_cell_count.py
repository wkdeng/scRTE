###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-30 23:29:01
 # @modify date 2023-05-26 10:48:21
 # @desc [description]
###
import sys
import math
import pandas as pd
import numpy as np
import os
from multiprocessing import Pool
import json
from collections import defaultdict

# sys.argv=['xx','../data/all_datasets','../www/mysql','../../universal_data/rmsk/rmsk_GRCh38.txt']

in_path=sys.argv[1]
out_path=sys.argv[2]
rmsk_f=sys.argv[3]
mode='append' if (len(sys.argv)==5 and sys.argv[5]=='append') else 'overwrite'

# load cell annotation
cell_annos=[os.path.join(in_path,x) for x in os.listdir(in_path) if x.endswith('.cell_umap.txt')]
cell_anno=pd.read_csv(cell_annos[0],sep='\t',index_col=0)
for x in cell_annos[1:]:
    cell_anno=pd.concat([cell_anno,pd.read_csv(x,sep='\t',index_col=0)],axis=0)
## replace value of Opc to OPC
cell_anno['predicted.celltype']=cell_anno['predicted.celltype'].replace('Opc','OPC')
for i in range(cell_umap.shape[0]):
    if cell_umap.iloc[i,1] !='Control':
        cell_umap.iloc[i,1]=cell_umap.iloc[i,7].split('_')[0]

# load rmsk
rmsk=pd.read_csv(rmsk_f,sep='\t')
rmsk=rmsk.loc[rmsk['repClass'].isin(['LINE','SINE','LTR']),:]
rmsk['repFamily']=rmsk['repFamily'].apply(lambda x: x.replace('?',''))
families=rmsk['repFamily'].unique()
subfams=rmsk['repName'].unique()

# load cell expression
cell_exps=[os.path.join(in_path,x) for x in os.listdir(in_path) if x.endswith('.cell_exp.txt')]

def load_cell_exp(cell_exp_f):
    cell_exp_i=pd.read_csv(cell_exp_f,sep='\t',index_col=0)
    subfam_cell_count_i={x:list(set(cell_exp_i.loc[cell_exp_i[x]>0,:].index)) if x in cell_exp_i.columns else [] for x in subfams}
    return subfam_cell_count_i

pool=Pool(20)
subfam_cell_count_x=pool.map(load_cell_exp,cell_exps)
pool.close()
pool.join()

if mode=='append' and os.path.isfile(os.path.join(in_path,'subfam_cell_count.json')):
    subfam_cell_count=json.load(open(os.path.join(in_path,'subfam_cell_count.json'),'r'))
else:
    subfam_cell_count=defaultdict(list)

for x in subfam_cell_count_x:
    for y in subfams:
        subfam_cell_count[y].extend(x[y])

json.dump(subfam_cell_count,open(os.path.join(in_path,'subfam_cell_count.json'),'w'))

fam_dic={}
te2family={}
for x in families:
    fam_dic[x]=rmsk.loc[rmsk['repFamily']==x,'repName'].unique().tolist()
    te2family.update({y:x for y in fam_dic[x]})
    
fam_cell_count={x:[] for x in fam_dic}

for x in fam_dic:
    for y in fam_dic[x]:
        if y in subfam_cell_count:
            fam_cell_count[x].extend(subfam_cell_count[y])
for x in fam_dic:
    fam_cell_count[x]=list(set(fam_cell_count[x]))


subfam_cell_count_mtx=pd.DataFrame(np.zeros([len(subfams),len(['Ex','In','Oli','OPC','Ast','Mic','Endo','VLMC'])]),columns=['Ex','In','Oli','OPC','Ast','Mic','Endo','VLMC'],index=subfams)
for x in subfam_cell_count:
    for y in subfam_cell_count[x]:
        subfam_cell_count_mtx.loc[x,cell_anno.loc[y,'predicted.celltype']]+=1
fam_cell_count_mtx=pd.DataFrame(np.zeros([len(families),len(['Ex','In','Oli','OPC','Ast','Mic','Endo','VLMC'])]),columns=['Ex','In','Oli','OPC','Ast','Mic','Endo','VLMC'],index=families)
for x in fam_cell_count:
    for y in fam_cell_count[x]:
        fam_cell_count_mtx.loc[x,cell_anno.loc[y,'predicted.celltype']]+=1
    
subfam_mtx_out=open(out_path+'/subfam_cellcount.sql','w')
subfam_mtx_out.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS SUBFAM_CELL_COUNT;
CREATE TABLE SUBFAM_CELL_COUNT (
    ID INT NOT NULL AUTO_INCREMENT,
    TE varchar(255) NOT NULL,
    TE_FAM varchar(255) NOT NULL,
    Ex FLOAT NOT NULL,
    `In` FLOAT NOT NULL,
    Oli FLOAT NOT NULL,
    OPC FLOAT NOT NULL,
    Ast FLOAT NOT NULL,
    Mic FLOAT NOT NULL,
    Endo FLOAT NOT NULL,
    VLMC FLOAT NOT NULL,
    PRIMARY KEY (ID)
);
''')
for i in range(subfam_cell_count_mtx.shape[0]):
    values=','.join([str(i) for i in subfam_cell_count_mtx.iloc[i,:]])
    te_fam=te2family[subfam_cell_count_mtx.index[i]]
    values='"'+subfam_cell_count_mtx.index[i]+'",'+f'"{te_fam}",'+values
    subfam_mtx_out.write(f'INSERT INTO SUBFAM_CELL_COUNT (TE,TE_FAM,Ex,`In`,Oli,OPC,Ast,Mic,Endo,VLMC) values({values});\n')
subfam_mtx_out.close()

fam_mtx_out=open(out_path+'/fam_cellcount.sql','w')
fam_mtx_out.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS FAM_CELL_COUNT;
CREATE TABLE FAM_CELL_COUNT (
    ID INT NOT NULL AUTO_INCREMENT,
    TE varchar(255) NOT NULL,
    Ex FLOAT NOT NULL,
    `In` FLOAT NOT NULL,
    Oli FLOAT NOT NULL,
    OPC FLOAT NOT NULL,
    Ast FLOAT NOT NULL,
    Mic FLOAT NOT NULL,
    Endo FLOAT NOT NULL,
    VLMC FLOAT NOT NULL,
    PRIMARY KEY (ID)
);
''')
for i in range(fam_cell_count_mtx.shape[0]):
    values=','.join([str(i) for i in fam_cell_count_mtx.iloc[i,:]])
    values='"'+fam_cell_count_mtx.index[i]+'",'+values
    fam_mtx_out.write(f'INSERT INTO FAM_CELL_COUNT (TE,Ex,`In`,Oli,OPC,Ast,Mic,Endo,VLMC) values({values});\n')
fam_mtx_out.close()

