###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-17 15:52:18
 # @modify date 2023-04-17 15:52:18
 # @desc [description]
###

import sys
import math
import pandas as pd

# sys.argv=['th','../data/3/cell_exp.txt','../www/mysql']
out_path=sys.argv[2]
cell_exp=pd.read_csv(sys.argv[1],sep='\t',index_col=0)

umap=cell_exp[['UMAP_1','UMAP_2']]
cell_exp=cell_exp.drop(['UMAP_1','UMAP_2'],axis=1)

exp_tables=[open(f'{out_path}/cell_exp_{i}.sql','w') for i in range(math.ceil((len(cell_exp.columns))/1000.0))]
gene_dict=open(f'{out_path}/gene_dict.sql','w')
gene_dict.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS GENE_DICT;
CREATE TABLE GENE_DICT (
    ID INT NOT NULL,
    GENE varchar(255) NOT NULL,
    TABLE_ID INT NOT NULL,
    PRIMARY KEY (ID) );\n''')

header=cell_exp.columns
for i in range(len(exp_tables)):
    exp_tables[i].write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS CELL_EXP_{i};
CREATE TABLE CELL_EXP_{i} (
ID INT NOT NULL,
CELL varchar(255) NOT NULL,\n'''.format(i=i))

for i in range(len(cell_exp.columns)):
    index=math.floor(i/1000.0)
    exp_tables[index].write(f'`{header[i]}` FLOAT NOT NULL,\n')
    gene_dict.write(f'INSERT INTO GENE_DICT values({i},"{header[i]}","{index}");\n')

for i in range(len(exp_tables)):
    exp_tables[i].write('UMAP_1 FLOAT NOT NULL,\n')
    exp_tables[i].write('UMAP_2 FLOAT NOT NULL,\n')
    exp_tables[i].write('PRIMARY KEY (ID) );\n')


import tqdm

for j in tqdm.tqdm(range(len(cell_exp.index))):
    cell=cell_exp.index[j]
    for i in range(len(exp_tables)):
        values=','.join([str(i) for i in cell_exp.loc[cell][i*1000:(i+1)*1000]])
        values+=','+str(umap.loc[cell][0])+','+str(umap.loc[cell][1])
        exp_tables[i].write(f'INSERT INTO CELL_EXP_{i} values({j},"{cell}",{values});\n')

for i in range(len(exp_tables)):
    exp_tables[i].close()
gene_dict.close()