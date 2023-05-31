###
# @author [Wankun Deng]
# @email [dengwankun@gmail.com]
# @create date 2023-04-10 14:41:40
# @modify date 2023-05-26 13:55:44
# @desc [description]
###

import sys
import pandas as pd
import random
from multiprocessing import Lock
from multiprocessing import Process
import os

# sys.argv=['th','../data/3/cell_umap.txt','../www/mysql/cell_umap.sql']
inpath = sys.argv[1]
out_path = sys.argv[2]
mode = 'overwrite' if len(sys.argv) < 4 else sys.argv[3]

# dataset=sys.argv[3]

if mode == 'append':
    data_cellumap = open(out_path, 'a')
else:
    data_cellumap = open(out_path, 'w')
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
data_cellumap.flush()

def process_a_file(file_path,lock):
    print(file_path)
    cell_umap = pd.read_csv(os.path.join(inpath, file_path), sep='\t')
    cell_umap['stage'] = cell_umap['stage'].astype(str)
    cell_umap['predicted.celltype'] = cell_umap['predicted.celltype'].replace(
        'Opc', 'OPC')
    for i in range(cell_umap.shape[0]):
        if cell_umap.iloc[i,1] =='Stage_0':
            cell_umap.iloc[i,1]='Control'
        if cell_umap.iloc[i,1] !='Control':
            cell_umap.iloc[i,1]=cell_umap.iloc[i,7].split('_')[0]

    for i in range(cell_umap.shape[0]):
        cell = cell_umap.index[i]
        cell_type, disease, stage, gender, age, umap_1, umap_2, dataset = cell_umap.loc[cell, [
            'predicted.celltype', 'Diagnosis', 'stage', 'msex', 'age_death', 'UMAP_1', 'UMAP_2', 'dataset']]
        with lock:
            data_cellumap.write(
                f'INSERT INTO DATA_CELLUMAP (scARE_ID,CELL,CELL_TYPE,DISEASE,STAGE,GENDER,AGE,UMAP_1,UMAP_2) values("{dataset}","{cell}","{cell_type}","{disease}","{stage}","{gender}","{age}","{umap_1}","{umap_2}");\n')

# for file_ in os.listdir(inpath):
#     if file_.endwith('.cell_umap.txt'):
lock=Lock()
files=[]
[files.append(file_) for file_ in os.listdir(inpath) if file_.endswith('.cell_umap.txt')]
processes = [Process(target=process_a_file, args=(file_,lock)) for file_ in files]
for p in processes:
    p.start()
for p in processes:
    p.join()

data_cellumap.close()
