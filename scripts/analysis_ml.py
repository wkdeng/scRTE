import warnings
warnings.filterwarnings('ignore')

import os
import sys
import pandas as pd
import numpy as np
from collections import defaultdict
from multiprocessing import Pool

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import scipy
from statsmodels.stats.multitest import multipletests

import scanpy as sc
import anndata
import scvelo as scv

from joblib import dump, load

from sklearn.model_selection import train_test_split,StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import * # roc_curve, auc, RocCurveDisplay
from functools import partial

os.chdir('/home/wdeng3/workspace/Codespace/scRTE/scripts/')

dataset='../data/all_datasets/AD_HS_00001.cell_exp.txt'
rmsk_f='../../universal_data/rmsk/rmsk_GRCh38.txt'
dataset_umap='../data/all_datasets/AD_HS_00001.cell_umap.txt'
gtf='../../universal_data/ref/GRCh38/gencode.v43.basic.annotation.gtf'

gene_type={}
for line in open(gtf):
    if not line.startswith('#'):
        info=line.strip().split('\t')
        if info[2]=='gene':
            split_='gene_name "' if 'gene_name' in info[-1] else 'gene_id "'
            gene_name=info[-1].split(split_)[1].split('"')[0]
            if 'lncRNA' in info[-1] :
                gene_type[gene_name]='lncRNA'
            elif 'protein_coding' in info[-1]:
                gene_type[gene_name]='protein_coding'
            elif 'pseudogene' in info[-1]:
                gene_type[gene_name]='pseudogene'
            else:
                gene_type[gene_name]='Others'
            
rmsk=pd.read_csv(rmsk_f,sep='\t')
rmsk['repFamily']=[x.replace('?','') for x in rmsk['repFamily']]
rmsk['repLen']=rmsk['genoEnd']-rmsk['genoStart']
classification=rmsk.loc[rmsk['repClass'].isin(['SINE', 'LINE', 'LTR']),['repName','repClass','repFamily']].drop_duplicates(ignore_index=True)
tmp=rmsk.iloc[:,[10,11]].drop_duplicates()
te_cls=dict(zip(tmp['repName'],tmp['repClass']))
tmp=rmsk.iloc[:,[10,11,12]].drop_duplicates()
tmp=tmp.loc[tmp['repClass'].isin(['SINE','LINE','LTR']),:]
te_fam=dict(zip(tmp['repName'],tmp['repFamily']))
fam_te=defaultdict(list)
for x in te_fam:
    fam_te[te_fam[x]].append(x)
gene_type.update(te_cls)
rtes=rmsk['repName'].unique()

genes=list(gene_type.keys())
genes_rep=[x.replace('_','.').replace('-','.') for x in genes]

## Read in data
sfg_ad=pd.read_csv('../data/all_datasets/AD_HS_00003.1.cell_exp.txt',sep='\t',index_col=0)
sfg_umap=pd.read_csv('../data/all_datasets/AD_HS_00003.1.cell_umap.txt',sep='\t',index_col=0)
colnames=sfg_ad.columns
repl_colnames=[]
for x in colnames:
    if '.' not in x or x not in genes_rep:
        repl_colnames.append(x)
    else:
        repl_colnames.append(genes[genes_rep.index(x)])

sfg_ad.columns=repl_colnames

sfg_ad['Diagnosis']=sfg_umap['Diagnosis']
sfg_ad['predicted.celltype']=sfg_umap['predicted.celltype']
sfg_ad['UMAP_1']=sfg_umap['UMAP_1']
sfg_ad['UMAP_2']=sfg_umap['UMAP_2']

ex_=sfg_ad.loc[sfg_ad['predicted.celltype']=='Ex',[x for x in sfg_ad.columns if x not in rtes]]
adata=anndata.AnnData(X=np.expm1(ex_.iloc[:,:-4]))

adata.obs['Diagnosis']=ex_['Diagnosis']
adata.obs['CellType']=ex_['predicted.celltype']
adata.obsm['X_umap']=ex_[['UMAP_1','UMAP_2']].to_numpy()
adata.var["mito"] = adata.var_names.str.startswith("MT-")
adata.layers["counts"] = adata.X.copy()
sc.pp.calculate_qc_metrics(adata, qc_vars=["mito"], inplace=True)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
# fig,axs=plt.subplots(1,3,figsize=[45,8])

non_mito=np.invert(adata.var_names.str.startswith("MT-"))
adata=adata[:,non_mito]
sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
# sc.pl.highly_variable_genes(adata)
sc.tl.pca(adata, svd_solver='arpack')
# sc.pl.pca(adata, color='CellType')
sc.tl.rank_genes_groups(adata, 'Diagnosis', method='t-test')
# sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)
gene_markers=[]
marker_list=np.array(adata.uns['rank_genes_groups']['names'].tolist()).flatten()
for i in marker_list:
    if i not in gene_markers:
        gene_markers.append(i)
extended_markers=gene_markers[:730*2]
gene_markers=gene_markers[:730]

## Define auc function
def cv_auc(classifiers,names,x,y,feature_name,index):
    print('Feature: %s'%feature_name)
    scaler = StandardScaler()
    classifier,model_name=classifiers[index],names[index]
    folds=[10] 

    font1 = {'family' : 'Arial',
            'weight' : 'normal',
            'size'   : 16}      
    figsize=6.2, 6.2
    figure, ax = plt.subplots(figsize=figsize)
    
    plt.tick_params(labelsize=18)
    plt_labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in plt_labels]
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',label='Luck', alpha=.8)

    for k in folds:
        kfold = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)   
        y_onehot=[]
        y_scores=[]
        for train,test in kfold.split(x, y):
            print('train: %s, test: %s' % (train, test))
            x[train] = scaler.fit_transform(x[train])
            x[test] = scaler.transform(x[test])
            label_binarizer = LabelBinarizer().fit(y[train])
            y_onehot_test = label_binarizer.transform(y[test])

            classifier.fit(x[train], 
                            y[train])
            probas_ = classifier.predict_proba(x[test])      
            y_onehot.extend(y_onehot_test.ravel())
            y_scores.extend(probas_.ravel()) 

        display = RocCurveDisplay.from_predictions(
            y_onehot,
            y_scores,
            name="%s-fold"%k,
            color="darkorange",
        )
        display.plot(ax=ax)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate', font1)
    plt.ylabel('True Positive Rate', font1)
    title='Micro-average OvR ROC Curve'
    plt.title(title, font1)
    plt.legend(loc="lower right")
    if not os.path.isdir('../data/analysis/models_%s'%feature_name):
        os.mkdir('../data/analysis/models_%s'%feature_name)
    plt.savefig( '../data/analysis/models_%s/%s_CV_roc.pdf' % (feature_name,model_name), dpi=300, bbox_inches = 'tight')
    # plt.show()
    return ['%s_%s'%(model_name, feature_name),y_onehot,y_scores]


## Caluculate 10-fold cross validation AUC for each feature

### Prepare data
cell='Ex'
cell_exp=sfg_ad.loc[sfg_ad['predicted.celltype']==cell,:]
cell_exp.iloc[:,:-4]=np.expm1(cell_exp.iloc[:,:-4].astype(float))
factors=pd.factorize(cell_exp['Diagnosis'])
labels=factors[0]
#### Expression profiles
rte_exp=cell_exp[[x for x in cell_exp.columns if x in rtes]]
gene_exp=cell_exp.loc[:,gene_markers]
combined_exp=cell_exp.loc[:,[x for x in cell_exp.columns if x in rtes]+gene_markers]
gene_exp2=cell_exp.loc[:,extended_markers]

### Define models
names = [
    "RBF SVM",
    "Random Forest",
    "AdaBoost",
    "MLP"
]

classifiers = [
    SVC(decision_function_shape='ovr',random_state=42,probability=True),
    RandomForestClassifier(n_estimators=100,random_state=42),
    AdaBoostClassifier(n_estimators=100,random_state=42),
    MLPClassifier(alpha=1, max_iter=10000,random_state=42,hidden_layer_sizes=(1000,1000))]

classifiers_gene= [
    SVC(decision_function_shape='ovr',random_state=42),
    RandomForestClassifier(n_estimators=100,random_state=42),
    AdaBoostClassifier(),
    MLPClassifier(alpha=1, max_iter=10000,random_state=42,hidden_layer_sizes=(1000,1000))
]

classifiers_combined= [
    SVC(decision_function_shape='ovr',random_state=42),
    RandomForestClassifier(n_estimators=100,random_state=42),
    AdaBoostClassifier(),
    MLPClassifier(alpha=1, max_iter=10000,random_state=42,hidden_layer_sizes=(1000,1000))
]

classifiers_gene2= [
    SVC(decision_function_shape='ovr',random_state=42),
    RandomForestClassifier(n_estimators=100,random_state=42),
    AdaBoostClassifier(),
    MLPClassifier(alpha=1, max_iter=10000,random_state=42,hidden_layer_sizes=(1000,1000))
]

### Cross validation
func_=partial(cv_auc,classifiers,names,rte_exp.to_numpy(),labels,'RTE730')
func_gene=partial(cv_auc,classifiers_gene,names,gene_exp.to_numpy(),labels,'Gene730')
func_combined=partial(cv_auc,classifiers_combined,names,combined_exp.to_numpy(),labels,'Combined')
func_gene2=partial(cv_auc,classifiers_gene2,names,gene_exp2.to_numpy(),labels,'Gene1460')

pool=Pool(4) 
ret=pool.map(func_,range(4))
ret_gene=pool.map(func_gene,range(4))
ret_combined=pool.map(func_combined,range(4))
ret_gene2=pool.map(func_gene2,range(4))
pool.close()
pool.join()