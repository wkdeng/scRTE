###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-06-30 13:17:49
 # @modify date 2023-07-12 11:12:52
 # @desc [description]
###
import os
import sys
import random
import numpy as np
import pandas as pd
from multiprocessing import Pool
from scipy.stats import mannwhitneyu

sys.argv=['th','../data/all_datasets','../www/mysql','../../universal_data/rmsk/rmsk_GRCh38.txt']
input_path=sys.argv[1]
output_path=sys.argv[2]
rmsk_f=sys.argv[3]

file_list=[x for x in os.listdir(input_path) if x.endswith('.cell_exp.txt')]
rmsk=pd.read_table(rmsk_f,sep='\t',header=None)
rtes=rmsk[rmsk[11].isin(['LINE','SINE','LTR'])][10].unique()
datasets=list(set([x.split('.')[0] for x in file_list]))
datasets.sort()
cell_types=['Ex','Ast','Mic','OPC','Oli','In']
def get_dataset(dataset):
    print(dataset)
    randint=random.randint(0,1000)
    print(f'loading data: {dataset}_{randint}')
    results=[]
    dt_ls=[x for x in file_list if x.startswith(dataset)]
    cell_exp=pd.read_table(os.path.join(input_path,dt_ls[0]),index_col=0)
    if len(dt_ls) >1:
        cell_umap=pd.read_table(f'{input_path}/{dataset}.1.cell_umap.txt',index_col=0)
        for i in range(1,len(dt_ls)):
            cell_exp=pd.concat([cell_exp,pd.read_table(f'{input_path}/'+dt_ls[i],index_col=0)])
            cell_umap=pd.concat([cell_umap,pd.read_table(f'{input_path}/{dataset}.{i}.cell_umap.txt',index_col=0)])
    else:
        cell_umap=pd.read_table(f'{input_path}/'+dataset+'.cell_umap.txt',index_col=0)
    
    cell_umap['predicted.celltype'] = cell_umap['predicted.celltype'].replace(
        'Opc', 'OPC')
    for i in range(cell_umap.shape[0]):
        if cell_umap.iloc[i,1] =='Stage_0':
            cell_umap.iloc[i,1]='Control'
        if cell_umap.iloc[i,1] !='Control':
            cell_umap.iloc[i,1]=cell_umap.iloc[i,7].split('_')[0]
    
    rte_rep=[x.replace('_','.').replace('-','.') for x in rtes]

    colnames=cell_exp.columns
    repl_colnames=[]
    for x in colnames:
        if '.' not in x or x not in rte_rep:
            repl_colnames.append(x)
        else:
            repl_colnames.append(rtes[rte_rep.index(x)])
    cell_exp.columns=repl_colnames

    
    cell_exp=cell_exp.loc[:,[x for x in cell_exp.columns if x in rtes]]
    ## disease v.s. control
    print('extracting disease v.s. control')
    disease=dataset.split('_')[0]
    for cell in cell_types:
        disease_list=cell_umap.loc[(cell_umap['predicted.celltype']==cell) & (cell_umap['Diagnosis']!='Control'),:].index
        control_list=cell_umap.loc[(cell_umap['predicted.celltype']==cell) & (cell_umap['Diagnosis']=='Control'),:].index
        for te in rtes:
            if te in cell_exp.columns:
                disease_exp=np.exp(cell_exp.loc[disease_list,te])
                control_exp=np.exp(cell_exp.loc[control_list,te])
                pval=mannwhitneyu(disease_exp,control_exp)[1]
                c1_median=np.mean(disease_exp)
                c2_median=np.mean(control_exp)
                pce1=np.count_nonzero(disease_exp>1)/(1.0*len(disease_exp))
                pce2=np.count_nonzero(control_exp>1)/(1.0*len(control_exp))
                fc=np.log2(np.mean(disease_exp)/np.mean(control_exp))
                results.append([te,f'{disease} v.s. Control',dataset,cell,'NA',np.log(c1_median),np.log(c2_median),fc,pval,pce1,pce2,len(disease_exp),len(control_exp)])
    ## cell v.s. cell
    print('extracting cell v.s. cell')
    for cell1 in cell_types:
        for cell2 in cell_types:
            if not cell1==cell2:
                for condition in [disease,'Control']:
                    cell1_list=cell_umap.loc[(cell_umap['predicted.celltype']==cell1) & (cell_umap['Diagnosis']==condition),:].index
                    cell2_list=cell_umap.loc[(cell_umap['predicted.celltype']==cell2) & (cell_umap['Diagnosis']==condition),:].index
                    for te in rtes:
                        if te in cell_exp.columns:
                            cell1_exp=np.exp(cell_exp.loc[cell1_list,te])
                            cell2_exp=np.exp(cell_exp.loc[cell2_list,te])
                            pval=mannwhitneyu(cell1_exp,cell2_exp)[1]
                            c1_median=np.mean(cell1_exp)
                            c2_median=np.mean(cell2_exp)
                            fc=np.log2(np.mean(cell1_exp)/np.mean(cell2_exp))
                            pce1=np.count_nonzero(cell1_exp>1)/(1.0*len(cell1_exp))
                            pce2=np.count_nonzero(cell2_exp>1)/(1.0*len(cell2_exp))
                            results.append([te,f'{cell1} v.s. {cell2}',dataset,'NA',condition,np.log(c1_median),np.log(c2_median),fc,pval,pce1,pce2,len(cell1_exp),len(cell2_exp)])
    return results

pool = Pool(20)
print(datasets)
ret=pool.map(get_dataset,datasets)
pool.close()
pool.join()

final_result=[]
for i in ret:
    final_result.extend(i)
final_result=pd.DataFrame(final_result,columns=['TE','Comparison','Dataset','Cell','Condition','log2_median1','log2_median2','log2_FC','pval','pce1','pce2','cell1_count','cell2_count'])

te_de=open(f'{output_path}/exp_de.sql','w')

te_de.write('''use scARE;
    DROP TABLE IF EXISTS `EXP_DE`;
    CREATE TABLE `EXP_DE` (
        `TE` varchar(255) NOT NULL,
        `COMPARISON` varchar(255) NOT NULL,
        `DATASET` varchar(255) NOT NULL,
        `CELL` varchar(255) NOT NULL,
        `CONDITION` varchar(255) NOT NULL,
        `MEAN1` float NOT NULL,
        `MEAN2` float NOT NULL,
        `FC` float NOT NULL,
        `PVAL` float NOT NULL,
        `PCE1` float NOT NULL,
        `PCE2` float NOT NULL,
        `CELL1_COUNT` int NOT NULL,
        `CELL2_COUNT` int NOT NULL);
        set autocommit=0;\n''')

count=0
values_list=[]
template='INSERT INTO `EXP_DE` (TE,COMPARISON,DATASET,CELL,`CONDITION`,MEAN1,MEAN2,`FC`,PVAL,PCE1,PCE2,CELL1_COUNT,CELL2_COUNT) VALUES {values};\n'
for i in range(final_result.shape[0]):
    if count==2000:
        te_de.write(template.format(values=','.join(values_list)))
        count=0
        values_list=[]
    row=list(final_result.iloc[i,:])
    row[:5]=['"'+str(x)+'"' for x in row[:5]]
    values_list.append('('+','.join([str(x) for x in row])+')')
    count+=1

if count>0:
    te_de.write(template.format(values=','.join(values_list)))
te_de.write('commit;')
te_de.close()  