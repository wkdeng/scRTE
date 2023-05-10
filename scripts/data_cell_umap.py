###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-10 14:41:40
 # @modify date 2023-04-10 14:41:40
 # @desc [description]
###

import sys
import pandas as pd
import random
# sys.argv=['th','../data/3/cell_umap.txt','../www/mysql/cell_umap.sql']
out_path=sys.argv[2]
cell_umap=pd.read_csv(sys.argv[1],sep='\t')
# dataset=sys.argv[3]

data_cellumap=open(out_path,'w')
data_cellumap.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS DATA_CELLUMAP;
CREATE TABLE DATA_CELLUMAP (
    ID INT NOT NULL AUTO_INCREMENT,
    scARE_ID varchar(255) NOT NULL,
    CELL varchar(255) NOT NULL,
    CELL_TYPE varchar(255) NOT NULL,
    DISEASE varchar(255) NOT NULL,
    STAGE varchar(255) NOT NULL,
    GENDER varchar(255) NOT NULL,
    AGE varchar(255) NOT NULL,
    UMAP_1 FLOAT NOT NULL,
    UMAP_2 FLOAT NOT NULL,
    PRIMARY KEY (ID) 
);
''')


import tqdm
cell_umap['stage']=cell_umap['stage'].astype(str)
for i in tqdm.tqdm(range(cell_umap.shape[0])):
    cell=cell_umap.index[i]
    cell_type,disease,stage,gender,age,umap_1,umap_2,dataset=cell_umap.loc[cell,['predicted.celltype','Diagnosis','stage','msex','age_death','UMAP_1','UMAP_2','dataset']]
    data_cellumap.write(f'INSERT INTO DATA_CELLUMAP (scARE_ID,CELL,CELL_TYPE,DISEASE,STAGE,GENDER,AGE,UMAP_1,UMAP_2) values("{dataset}","{cell}","{cell_type}","{disease}","{stage}","{gender}","{age}","{umap_1}","{umap_2}");\n')
data_cellumap.close()