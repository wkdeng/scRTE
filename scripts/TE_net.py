###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-21 14:16:13
 # @modify date 2023-03-21 14:16:13
 # @desc [description]
###
from pybedtools import BedTool
import sys
import pandas as pd
# sys.argv=['test.opy','../../universal_data/rmsk/rmsk_GRCh38.txt','../../universal_data/ref/GRCh38/genes.bed']
rmsk=sys.argv[1]
gene_anno=sys.argv[2]
out=sys.argv[3]

rmsk_df=pd.read_csv(rmsk,sep='\t')
rmsk_df['index']=rmsk_df[['repClass','repFamily','repName']].agg(':'.join,axis=1)

rmsk_bed=BedTool.from_dataframe(rmsk_df[['genoName','genoStart','genoEnd','index','swScore','strand']])
conn=rmsk_bed.intersect(anno_bed,s=True,wa=True,wb=True).to_dataframe()
conn[['ensg','gn']]=[x.split(':') for x in conn['blockCount']]
conn[['name','gn']].to_csv(out,header=True,index=False)