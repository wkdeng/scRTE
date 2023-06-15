###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-18 16:18:04
 # @modify date 2023-05-31 15:17:02
 # @desc [description]
###
import sys
import pandas as pd
from multiprocessing import Pool
import os
from multiprocessing import Lock

# sys.argv=['xx','../data/all_datasets','../../universal_data/rmsk/rmsk_GRCh38.txt','../www/mysql']

in_path=sys.argv[1]
rmsk_f=sys.argv[2]
out_path=sys.argv[3]

te_table=pd.read_csv(rmsk_f,sep='\t')
te_table['repFamily']=te_table['repFamily'].apply(lambda x: x.replace('?',''))

rte=set(te_table.loc[te_table['repClass'].isin(['LINE','SINE','LTR']),['repName','repClass','repFamily']].drop_duplicates()['repName'].tolist())

# load cell expression
cell_exps=[os.path.join(in_path,x) for x in os.listdir(in_path) if x.endswith('.cell_exp.txt')]
def load_cell_exp(cell_exp_f):
    cell_exp_i=pd.read_csv(cell_exp_f,sep='\t',index_col=0)
    cell_exp_i=cell_exp_i.loc[:,cell_exp_i.columns.isin(rte)]
    return cell_exp_i
pool=Pool(20)
cell_exps=pool.map(load_cell_exp,cell_exps)
pool.close()
pool.join()
cell_exp=pd.concat(cell_exps,axis=0)

# load cell umap
cell_umaps=[os.path.join(in_path,x) for x in os.listdir(in_path) if x.endswith('.cell_umap.txt')]
cell_umap=pd.concat([pd.read_csv(x,sep='\t',index_col=0) for x in cell_umaps],axis=0)
## replace value of Opc to OPC
cell_umap['predicted.celltype']=cell_umap['predicted.celltype'].replace('Opc','OPC')
for i in range(cell_umap.shape[0]):
    if cell_umap.iloc[i,1] =='Stage_0':
        cell_umap.iloc[i,1]='Control'
    if cell_umap.iloc[i,1] !='Control':
        cell_umap.iloc[i,1]=cell_umap.iloc[i,7].split('_')[0]

datasets=set(cell_umap['dataset'].tolist())
diagnosis=set(cell_umap['Diagnosis'].tolist())
cell_types=set(cell_umap['predicted.celltype'].tolist())


def process(arg):
    disease,dataset,cell_type=arg
    cells=cell_umap.loc[(cell_umap['dataset']==dataset)&(cell_umap['Diagnosis']==disease)&(cell_umap['predicted.celltype']==cell_type),:].index.tolist()
    rows=[]
    for te in cell_exp.columns:
        row=[]
        row.append(cell_type)
        row.append(len(cells))
        row.append(dataset)
        row.append(disease)
        row.append(te)
        row.append(cell_exp.loc[cells,te].max())
        row.append(cell_exp.loc[cells,te].min())
        row.extend(list(cell_exp.loc[cells,te].quantile([0.25,0.5,0.75])))
        rows.append(row)
    return rows
    
pool=Pool(40)
ret=pool.map(process,cell_umap[['Diagnosis','dataset','predicted.celltype']].drop_duplicates().to_numpy())
pool.close()
pool.join()

result=[]
for item in ret:
    result.extend(item)
    
te_exp=open(out_path+'/te_exp_boxplot.sql','w')

te_exp.write('''use scARE;
    DROP TABLE IF EXISTS `TE_EXP_BOXPLOT`;
    CREATE TABLE `TE_EXP_BOXPLOT` (
        ID int(11) NOT NULL AUTO_INCREMENT,
        CELL_TYPE varchar(255) NOT NULL,
        CELL_NUM int(11) NOT NULL,
        DATASET varchar(255) NOT NULL,
        DISEASE varchar(255) NOT NULL,
        TE varchar(255) NOT NULL,
        MAX float NOT NULL,
        MIN float NOT NULL,
        Q1 float NOT NULL,
        MEDIAN float NOT NULL,
        Q3 float NOT NULL,
        PRIMARY KEY (ID));
        set autocommit=0;\n''')

result=pd.DataFrame(result,columns=['cell_type','cell_num','dataset','disease','te','max','min','q1','median','q3'])
result['cell_type']=result['cell_type'].apply(lambda x:'"'+x+'"')
result['dataset']=result['dataset'].apply(lambda x:'"'+x+'"')   
result['disease']=result['disease'].apply(lambda x:'"'+x+'"')
result['te']=result['te'].apply(lambda x:'"'+x+'"')
result.fillna(-1,inplace=True)

count=0
values_list=[]
template='INSERT INTO `TE_EXP_BOXPLOT` (CELL_TYPE,CELL_NUM,DATASET,DISEASE,TE,MAX,MIN,Q1,MEDIAN,Q3) VALUES {values};\n'
for i in range(result.shape[0]):
    if count==2000:
        te_exp.write(template.format(values=','.join(values_list)))
        count=0
        values_list=[]
    values_list.append('('+','.join([str(x) for x in result.iloc[i,:]])+')')
    count+=1

if count>0:
    te_exp.write(template.format(values=','.join(values_list)))
te_exp.write('commit;')
te_exp.close()