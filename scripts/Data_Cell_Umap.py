###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-10 14:41:40
 # @modify date 2023-04-10 14:41:40
 # @desc [description]
###

import sys
import pandas as pd

# sys.argv=['th','../data/3/cell_umap.txt','../www/mysql/cell_umap.sql']
out_path=sys.argv[2]
cell_umap=pd.read_csv(sys.argv[1],sep='\t')


data_cellumap=open(out_path,'w')
data_cellumap.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS DATA_CELLUMAP;
CREATE TABLE DATA_CELLUMAP (
    ID INT NOT NULL AUTO_INCREMENT,
    DATASET varchar(255) NOT NULL,
    CELL varchar(255) NOT NULL,
    CELL_TYPE varchar(255) NOT NULL,
    UMAP_1 FLOAT NOT NULL,
    UMAP_2 FLOAT NOT NULL,
    PRIMARY KEY (ID) 
);
''')


import tqdm

for cell in tqdm.tqdm(cell_umap.index):
    dataset,cell_type,umap_1,umap_2=cell_umap.loc[cell,['orig.ident','predicted.celltype','UMAP_1','UMAP_2']]
    data_cellumap.write(f'INSERT INTO DATA_CELLUMAP (DATASET,CELL,CELL_TYPE,UMAP_1,UMAP_2) values("{dataset}","{cell}","{cell_type}","{umap_1}","{umap_2}");\n')
data_cellumap.close()