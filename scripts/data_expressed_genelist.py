###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-07-05 11:53:34
 # @modify date 2023-07-07 11:14:31
 # @desc [description]
###
import sys
import pandas as pd
import os
from collections import defaultdict

# sys.argv=['th','../data/all_datasets','../www/mysql','../../universal_data/ref/GRCh38/gencode.v43.basic.annotation.gtf','../../universal_data/rmsk/rmsk_GRCh38.txt']
inpath=sys.argv[1]
out_path=sys.argv[2]
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
genes_rep=[x.replace('_','.').replace('-','.') for x in genes]

for file_ in os.listdir(inpath):
    if file_.endswith('cell_exp.txt'):
        fl=open(inpath+'/'+file_,'r').readline().strip().split('\t')
        fl=fl[:-2]
        repl_colnames=[]
        for x in fl:
            if '.' not in x or x not in genes_rep:
                repl_colnames.append(x)
            else:
                repl_colnames.append(genes[genes_rep.index(x)])
        gene_list[file_.split('.')[0]]=repl_colnames

for key in gene_list:
    with open(out_path+'/'+key+'.txt','w') as f:
        f.write(','.join(gene_list[key]))