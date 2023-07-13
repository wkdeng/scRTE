###
# @author [Wankun Deng]
# @email [dengwankun@gmail.com]
# @create date 2023-04-10 14:41:40
# @modify date 2023-07-05 10:56:20
# @desc [description]
###

import sys
import math
import tqdm
import pandas as pd
import os
import json
from collections import defaultdict

# sys.argv=['th','../data/all_datasets','../www/mysql','overwrite','../../universal_data/ref/GRCh38/gencode.v43.basic.annotation.gtf','../../universal_data/rmsk/rmsk_GRCh38.txt']
inpath=sys.argv[1]
out_path=sys.argv[2]
mode='append' if sys.argv[3]=='append' else 'overwrite'
gtf=sys.argv[4]
rmsk_f=sys.argv[5]
chunck_size=900.0
if mode=='overwrite':
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

    exp_tables=[open(f'{out_path}/cell_exp_{i}.sql','w') for i in range(math.ceil((len(genes))/chunck_size))]
    for i in range(len(exp_tables)):
        exp_tables[i].write('''CREATE DATABASE IF NOT EXISTS scARE;
                                USE scARE;
                                DROP TABLE IF EXISTS CELL_EXP_{i}; 
                                CREATE TABLE CELL_EXP_{i} (
                                scARE_ID varchar(255) NOT NULL,
                                CELL varchar(255) NOT NULL,\n'''.format(i=i))
        
    gene_dict=open(f'{out_path}/gene_dict.sql','w') 
    gene_dict.write('''\
            CREATE DATABASE IF NOT EXISTS scARE;
            USE scARE;
            DROP TABLE IF EXISTS GENE_DICT;
            CREATE TABLE GENE_DICT (
                GENE varchar(255) NOT NULL,
                TABLE_ID INT NOT NULL);\n''')

    table_genes=defaultdict(list)
    for i in range(len(genes)):
        index=math.floor(i/chunck_size)
        exp_tables[index].write(f'`{genes[i]}` FLOAT DEFAULT 0,\n')
        table_genes[index].append(genes[i])
        gene_dict.write(f'INSERT INTO GENE_DICT values("{genes[i]}","{index}");\n')
    for i in range(len(exp_tables)):
        exp_tables[i].write('UMAP_1 FLOAT NOT NULL,\n')
        exp_tables[i].write('UMAP_2 FLOAT NOT NULL);\n')
        # exp_tables[i].write('set autocommit=0;\n')
        exp_tables[i].flush()
    json.dump(table_genes,open(f'{out_path}/table_genes.json','w'))
else:
    table_genes=json.load(open(f'{out_path}/table_genes.json','r'))
    exp_tables=[open(f'{out_path}/cell_exp_{i}.sql','a') for i in range(len(table_genes))]


def one_table(i):
    expressed_i=[x for x in cell_exp.columns if x in table_genes[i]]+['UMAP_1','UMAP_2']
    tmp_exp=pd.DataFrame(columns=(['scARE_ID','CELL']+expressed_i),index=cell_exp.index)
    tmp_exp['scARE_ID']=['"%s"'%cell_dataset[x] for x in cell_exp.index]
    tmp_exp['CELL']=['"%s"'%x for x in cell_exp.index]
    tmp_exp.loc[:,expressed_i]=cell_exp.loc[:,expressed_i]
    all_values=tmp_exp.agg(lambda x:  ','.join(x.astype(str)), axis=1).values
    expressed_i_c='`,`'.join(expressed_i)
    template=f'''INSERT INTO CELL_EXP_{i} (scARE_ID,CELL,`{expressed_i_c}`) values '''

    count=0
    values_list=[]
    to_write=''
    for x in all_values:
        if count==80:
            to_write+=template+','.join(values_list)+';\n'
            count=0
            values_list=[]
        values_list.append('('+x+')')
        count+=1
    if len(values_list)>0:
        to_write+=template+','.join(values_list)+';\n'
    # to_write='\n'.join([template.format(i=i,expressed_i_c=expressed_i_c,values=x) for x in all_values])+'\n'
    exp_tables[i].write(to_write)

from multiprocessing import Pool

genes_rep=[x.replace('_','.').replace('-','.') for x in genes]
for file_ in os.listdir(inpath):
    if file_.endswith('.cell_exp.txt'):
        cell_exp=pd.read_csv(os.path.join(inpath,file_),sep='\t',index_col=0)
        colnames=cell_exp.columns
        repl_colnames=[]
        for x in colnames:
            if '.' not in x or x not in genes_rep:
                repl_colnames.append(x)
            else:
                repl_colnames.append(genes[genes_rep.index(x)])
        cell_exp.columns=repl_colnames
        cell_dataset=pd.read_csv(os.path.join(inpath,file_.replace('cell_exp','cell_umap')),sep='\t',index_col=0)['dataset'].to_dict()
        pool=Pool(40)
        pool.map(one_table,range(len(exp_tables)))
        pool.close()
        pool.join()

[x.write('commit;\n') for x in exp_tables]
[x.flush() for x in exp_tables]
[x.close() for x in exp_tables]