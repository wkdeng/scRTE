###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-21 14:16:13
 # @modify date 2023-05-22 15:45:59
 # @desc [description]
###
import sys
import tqdm

import pandas as pd
from pybedtools import BedTool
from collections import defaultdict
import networkx as nx
from networkx.readwrite import json_graph

# sys.argv=['test.opy','../../universal_data/rmsk/rmsk_GRCh38.txt','../../universal_data/ref/GRCh38/genes.bed']
rmsk=sys.argv[1]
gene_anno=sys.argv[2]
out=sys.argv[3]
net_out=sys.argv[4]

rmsk_df=pd.read_csv(rmsk,sep='\t')
rmsk_df['repFamily']=rmsk_df['repFamily'].apply(lambda x: x.replace('?',''))
rmsk_df['index']=rmsk_df[['repClass','repFamily','repName']].agg(':'.join,axis=1)


rmsk_bed=BedTool.from_dataframe(rmsk_df[['genoName','genoStart','genoEnd','index','swScore','strand']])
conn=rmsk_bed.intersect(gene_anno,s=True,wa=True,wb=True).to_dataframe()
conn[['ensg','gn']]=[x.split(':') for x in conn['blockCount']]

print(len(conn))
conn['class']=[x.split(':')[0] for x in conn['name']]
conn=conn.loc[conn['class'].isin(['SINE','LTR','LINE'])]
conn=conn[['name','gn']].drop_duplicates()
conn[['name','gn']].to_csv(net_out,header=True,index=False)

network=pd.read_csv(net_out,sep=',')
idx=list(set(network['name']))

g=nx.read_adjlist(net_out,delimiter=',',nodetype=str)

te_net=open(out,'w')
te_net.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS TE_NET;
CREATE TABLE TE_NET (
    ID INT NOT NULL AUTO_INCREMENT,
    CLASS varchar(255) NOT NULL,
    FAMILY varchar(255) NOT NULL,
    NAME varchar(255) NOT NULL,
    D1 longtext NOT NULL,
    D2 longtext NOT NULL,
    PRIMARY KEY (ID) 
);
''')

for node_id in tqdm.tqdm(idx):
    Ds=[]
    for i in range(2):
        subgraph = g.subgraph(nx.single_source_shortest_path_length(g, node_id, cutoff=i+1).keys())
        data = json_graph.node_link_data(subgraph)
        for item in data['nodes']:
            if item['id'].startswith('SINE') or item['id'].startswith('LINE') or item['id'].startswith('LTR'):
                item['group']=1
            else:
                item['group']=0
                                
        # remove 'directed','multigraph','graph' from data
        data.pop('directed')
        data.pop('multigraph')
        data.pop('graph')
        data=str(data).replace("'", '\\"')
        Ds.append(data)
    class_, family, name =node_id.split(':')
    D1,D2=Ds
    te_net.write(f'INSERT INTO TE_NET (CLASS,FAMILY,NAME,D1,D2) VALUES ("{class_}","{family}","{name}","{D1}","{D2}");\n')
te_net.close()
