###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-30 23:29:01
 # @modify date 2023-04-30 23:29:01
 # @desc [description]
###
import sys
import math
import pandas as pd
import numpy as np

# sys.argv=['th','../data/3/cell_exp.txt','../www/mysql','../../universal_data/rmsk/rmsk_GRCh38.txt','../data/3/cell_umap.txt']
out_path=sys.argv[2]
cell_exp=pd.read_csv(sys.argv[1],sep='\t',index_col=0)
rmsk=pd.read_csv(sys.argv[3],sep='\t')
rmsk=rmsk.loc[rmsk['repClass'].isin(['LINE','SINE','LTR']),:]
cell_anno=pd.read_csv(sys.argv[4],sep='\t',index_col=0)

families=rmsk['repFamily'].unique()
subfams=rmsk['repName'].unique()

subfam_cell_count={x:list(set(cell_exp.loc[cell_exp[x]>0,:].index)) if x in cell_exp.columns else [] for x in subfams}
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

subfam_cell_count_mtx=pd.DataFrame(np.zeros([len(subfams),len(['Ex','In','Oli','Opc','Ast','Mic','Per'])]),columns=['Ex','In','Oli','Opc','Ast','Mic','Per'],index=subfams)
for x in subfam_cell_count:
    for y in subfam_cell_count[x]:
        subfam_cell_count_mtx.loc[x,cell_anno.loc[y,'predicted.celltype']]+=1
fam_cell_count_mtx=pd.DataFrame(np.zeros([len(families),len(['Ex','In','Oli','Opc','Ast','Mic','Per'])]),columns=['Ex','In','Oli','Opc','Ast','Mic','Per'],index=families)
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
    Opc FLOAT NOT NULL,
    Ast FLOAT NOT NULL,
    Mic FLOAT NOT NULL,
    Per FLOAT NOT NULL,
    PRIMARY KEY (ID)
);
''')
for i in range(subfam_cell_count_mtx.shape[0]):
    values=','.join([str(i) for i in subfam_cell_count_mtx.iloc[i,:]])
    te_fam=te2family[subfam_cell_count_mtx.index[i]]
    values='"'+subfam_cell_count_mtx.index[i]+'",'+f'"{te_fam}",'+values
    subfam_mtx_out.write(f'INSERT INTO SUBFAM_CELL_COUNT (TE,TE_FAM,Ex,`In`,Oli,Opc,Ast,Mic,Per) values({values});\n')
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
    Opc FLOAT NOT NULL,
    Ast FLOAT NOT NULL,
    Mic FLOAT NOT NULL,
    Per FLOAT NOT NULL,
    PRIMARY KEY (ID)
);
''')
for i in range(fam_cell_count_mtx.shape[0]):
    values=','.join([str(i) for i in fam_cell_count_mtx.iloc[i,:]])
    values='"'+fam_cell_count_mtx.index[i]+'",'+values
    fam_mtx_out.write(f'INSERT INTO FAM_CELL_COUNT (TE,Ex,`In`,Oli,Opc,Ast,Mic,Per) values({values});\n')
fam_mtx_out.close()

