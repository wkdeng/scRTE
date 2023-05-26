###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-17 14:53:15
 # @modify date 2023-05-22 15:42:35
 # @desc [description]
###
import pandas as pd 
import sys
from collections import defaultdict
import re
import numpy as np
from tqdm import tqdm
import json
from pybedtools import BedTool

# sys.argv=['script.py','../../universal_data/rmsk/rmsk_GRCh38.txt','../data/website/Dfam.embl','../www/mysql/te_basic.sql','../../universal_data/ref/GRCh38/STAR/chrNameLength.txt']
rmsk=sys.argv[1]
consensus=sys.argv[2]
output=sys.argv[3]
chr_len_f=sys.argv[4]
te_table=pd.read_csv(rmsk,sep='\t')
gene_anno=sys.argv[5]


te_basic=open(output,'w')
te_basic.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS TE_BASIC;
CREATE TABLE TE_BASIC (
    ID INT NOT NULL AUTO_INCREMENT,
    CLASS varchar(255) NOT NULL,
    FAMILY varchar(255) NOT NULL,
    NAME varchar(255) NOT NULL,
    CONSENSUS TEXT,
    CONSENSUS_LEN INT,
    NUM_OCCUR INT NOT NULL,
    OCCUR_CHR JSON NOT NULL,
    DISTRIBUTION_EA_CHR JSON NOT NULL,
    DISTRIBUTION_GENE JSON NOT NULL,
    PRIMARY KEY (ID) 
);
''')

rte=te_table.loc[te_table['repClass'].isin(['LINE','SINE','LTR']),['repName','repClass','repFamily']].drop_duplicates()
rte['repFamily']=rte['repFamily'].apply(lambda x: x.replace('?',''))
## get consensus squence from Dfam, need to align TE names.
rte_consensus=defaultdict(lambda:defaultdict(str))
cname=''
ctype=''
cfam=''
cseq=''
for line in open(consensus):
    if line.startswith('//'):
        if len(cname) >0 :
            # if cname in rte['repName']:
            rte_consensus[cfam][cname]=cseq
            cname=''
            ckw=''
            cseq=''
            cac=''
    elif line.startswith('NM'):
        cname=line.strip().split(' ')[-1]
    elif line.startswith('CC        Type: '):
        ctype=line.strip().split(' ')[-1]
    elif line.startswith('CC        SubType: '):
        cfam=line.strip().split(' ')[-1]
    elif line.startswith('     '):
        cseq+=re.sub(r'[\d\s]','',line.strip())
    elif line.startswith('DR'):
        if 'Repbase' in line:
            cname=line.split('Repbase;')[1].strip()[:-1]    

rte['Consensus']=''
rte['Consensus_len']=np.zeros(len(rte))
count=0
for i in range(len(rte)):
    name,family=rte.iloc[i,[0,2]]
    seq=rte_consensus[family][name]
    seq_len=len(seq)
    if seq_len == 0:
        seq='N/A'
        # seq_len=np.nan
        count+=1
    rte.iloc[i,[3,4]]=[seq,seq_len]

## get index for te in gene/intergenic region
genes=BedTool(gene_anno)
# cdss=BedTool(cds_anno)
# utrs=BedTool(utr_anno)
# utrs=utrs.subtract(cdss,s=True)
te_table['order']=range(len(te_table))
te_bed=BedTool.from_dataframe(te_table[['genoName','genoStart','genoEnd','order','swScore','strand']])
gene_te_index=te_bed.intersect(genes,wa=True,u=True,s=True,f=0.5).to_dataframe()['name']
# cds_te_index=te_bed.intersect(cdss,wa=True,u=True,s=True,f=0.5).to_dataframe()['name']
# utr_te_index=te_bed.intersect(utrs,wa=True,u=True,s=True,f=0.5).to_dataframe()['name']


## get number/distribution for each rte
valid_chr=['chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM']
chr_len={x[0]:int(x[1]) for x in [y.strip().split('\t') for y in open(chr_len_f)]}
chr_len['others']=-1

hit_dict=defaultdict(int)
chr_count=defaultdict(lambda:[0]*(len(valid_chr)+1))
chr_dist=defaultdict(lambda:np.zeros((len(valid_chr),100)))
gene_dist=defaultdict(lambda:[0,0])
for i in tqdm(range(len(te_table))):
    info=te_table.iloc[i,:]
    index="%s:%s"%(info[10],info[12])
    hit_dict[index]+=1
    chr_=info[5]
    chr_=chr_ if chr_ in valid_chr else 'others'
    if i in gene_te_index:
        gene_dist[index][0]+=1
    else:
        gene_dist[index][1]+=1
    if chr_ in valid_chr:
        position=int((info[6]+info[7])*100/(2.0*chr_len[chr_]))
        chr_dist[index][valid_chr.index(chr_)][position]+=1
        chr_count[index][valid_chr.index(chr_)]+=1
    else:
        chr_count[index][-1]+=1

rte['index']=rte[['repName','repFamily']].agg(':'.join,axis=1)
rte['NumLocus']=[hit_dict[x] for x in rte['index']]
rte['occur_chr']=[json.dumps(chr_count[index]) for index in rte['index']]
rte['chr_dist']=[json.dumps(chr_dist[index].tolist()) for index in rte['index']]
rte['gene_dist']=[json.dumps(gene_dist[index]) for index in rte['index']]


for i in range(len(rte)):
    class_, family, name, consensus, consensus_len, num_occur, occur_chr, dist_ea_chr, dist_gene =rte.iloc[i,[1,2,0,3,4,6,7,8,9]]
    te_basic.write(f'INSERT INTO TE_BASIC (CLASS,FAMILY,NAME,CONSENSUS,CONSENSUS_LEN,NUM_OCCUR,OCCUR_CHR,DISTRIBUTION_EA_CHR,DISTRIBUTION_GENE) VALUES \
        ("{class_}","{family}","{name}","{consensus}","{consensus_len}","{num_occur}","{occur_chr}","{dist_ea_chr}","{dist_gene}");\n')
te_basic.close()
