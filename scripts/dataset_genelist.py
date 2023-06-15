###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-06-07 09:32:41
 # @modify date 2023-06-12 09:29:52
 # @desc [description]
###

import os
import sys
from collections import defaultdict
import pandas as pd

in_folder = sys.argv[1]
out_file = open(sys.argv[2],'w')
gtf=sys.argv[3]
rmsk_f=sys.argv[4]

genes=[]
for line in open(gtf): 
    if not line.startswith('#'):
        info=line.strip().split('\t')
        if info[2]=='gene' and ('lncRNA' in info[-1] or 'protein_coding' in info[-1]):
            split_='gene_name "' if 'gene_name' in info[-1] else 'gene_id "'
            genes.append(info[-1].split(split_)[1].split('"')[0])            

rmsk=pd.read_csv(rmsk_f,sep='\t',header=None)
rmsk=rmsk[rmsk[11].isin(['LINE','SINE','LTR'])]
genes.extend(rmsk[10].unique())
genes=list(set(genes))


gene_list=defaultdict(list)
for file_ in os.listdir(in_folder):
    if file_.endswith('.cell_exp.txt'):
        for line in open(os.path.join(in_folder,file_)):
            gene_list[file_.split('.')[0]].extend(line.strip().split('\t'))
            break
    
out_file.write('''
            CREATE DATABASE IF NOT EXISTS scARE;
            USE scARE;
            DROP TABLE IF EXISTS GENE_LIST;
            CREATE TABLE GENE_LIST (
                DATASET varchar(255) NOT NULL,
                LIST TEXT NOT NULL);\n''')
                
for dataset in gene_list:
    gene_list[dataset]=[x for x in list(set(gene_list[dataset])) if x in genes]
    print(dataset,len(gene_list[dataset]))
    out_file.write(f"INSERT INTO GENE_LIST VALUES ('{dataset}','{','.join(gene_list[dataset])}');\n")
out_file.close()
    