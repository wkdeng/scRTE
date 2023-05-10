###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-21 13:46:24
 # @modify date 2023-04-21 13:46:24
 # @desc [description]
###

import sys
import tqdm
import pandas as pd
import numpy as np


out=sys.argv[2]

network=pd.read_csv(sys.argv[1],sep=',')
network[['class','family','te_name']]=np.array([x.split(':') for x in network['name']])

te_gene=open(out,'w')
te_gene.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS TE_GENE;
CREATE TABLE TE_GENE (
    ID INT NOT NULL AUTO_INCREMENT,
    CLASS varchar(255) NOT NULL,
    FAMILY varchar(255) NOT NULL,
    NAME varchar(255) NOT NULL,
    GENE varchar(255) NOT NULL,
    PRIMARY KEY (ID) 
);
''')

for i in tqdm.tqdm(range(len(network))):
    class_,family,name,gene=network.iloc[i][['class','family','te_name','gn']]
    te_gene.write(f'INSERT INTO TE_GENE (CLASS,FAMILY,NAME,GENE) VALUES ("{class_}","{family}","{name}","{gene}");\n')
te_gene.close()
