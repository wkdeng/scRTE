import pandas as pd
import numpy as np
import sys
import os
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score,StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import * # roc_curve, auc, RocCurveDisplay
from sklearn.preprocessing import LabelBinarizer
from functools import partial
from multiprocessing import Pool
import matplotlib.pyplot as plt
from itertools import compress

def cv_thread(classifier,data):
    print('Thread started.')
    scaler = StandardScaler()
    y_onehot=[]
    y_score=[]
    train_x,test_x,train_y,test_y=data
    # print('train: %s, test: %s' % (train, test))
    train_x = scaler.fit_transform(train_x)
    test_x = scaler.transform(test_x)
    label_binarizer = LabelBinarizer().fit(train_y)
    y_onehot_test = label_binarizer.transform(test_y)
    classifier.fit(train_x, train_y)
    probas_ = classifier.predict_proba(test_x)      
    y_onehot.extend(y_onehot_test.ravel())
    y_score.extend(probas_.ravel()) 
    return y_onehot,y_score

def split_dataset(X,y,k):
    kfold = StratifiedKFold(n_splits=k, shuffle=True, random_state=42) 
    datasets=[]
    for train,test in kfold.split(X, y):
        datasets.append([X[train],X[test],y[train],y[test]])
    return datasets

def cv_auc_core(classifier,X,y,output):
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
        y_onehots,y_scores=[],[]
        pool=Pool(k)
        ret=pool.map(partial(cv_thread,classifier),split_dataset(X,y,k))
        pool.close()
        pool.join()
        for lst in ret:
            y_onehots.extend(lst[0])
            y_scores.extend(lst[1])
        display = RocCurveDisplay.from_predictions(
            y_onehots,
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
    plt.savefig(output, dpi=300, bbox_inches = 'tight')
    return [y_onehots,y_scores]

def cv_auc(classifiers,names,X,y,feature_name,index):
    classifier,model_name=classifiers[index],names[index]
    if not os.path.isdir('../data/analysis/models_%s'%feature_name):
        os.mkdir('../data/analysis/models_%s'%feature_name)
    y_onehots,y_scores=cv_auc_core(classifier,X,y,'../data/analysis/models_%s/%s_CV_roc.pdf' % (feature_name,model_name))
    return [y_onehots,y_scores]

n_features_to_select=int(sys.argv[1])
n_features_to_select_from=int(sys.argv[2]  )
cell_exp=pd.read_csv('../data/analysis/combined_exp1460.txt',sep='\t')
sfg_umap=pd.read_csv('../data/all_datasets/AD_HS_00003.1.cell_umap.txt',sep='\t',index_col=0)
sfg_umap=sfg_umap.loc[sfg_umap['predicted.celltype']=='Ex',:]
factors=pd.factorize(sfg_umap['Diagnosis'])
labels=factors[0]

clmns=list(cell_exp.columns)
valid_features=clmns[:n_features_to_select_from]
valid_features.extend(clmns[730:730+n_features_to_select_from])
rfe = RFE(estimator=RandomForestClassifier(n_estimators=100,random_state=42), n_features_to_select=n_features_to_select)
model=RandomForestClassifier(n_estimators=100,random_state=42)
pipeline = Pipeline(steps=[('s',rfe),('m',model)])
cv_auc_core(pipeline,cell_exp[valid_features].to_numpy(),labels,
            '../data/analysis/models_rfe%s_%s/cv10.pdf'%(n_features_to_select,n_features_to_select_from))

pipeline.fit(cell_exp[valid_features].to_numpy(),labels)
importances = pipeline.named_steps['m'].feature_importances_

index=list(compress(valid_features,list(pipeline[0].support_)))
importances=pd.Series(importances, index=index)
importances=pd.concat([importances, 
                       pd.Series(np.std([tree.feature_importances_ for tree in pipeline.named_steps['m'].estimators_], axis=0),
                                 index=index)], axis=1)
importances.columns=['Importance','STD']

importances=importances.sort_values(by='Importance',ascending=False)
importances_=importances.iloc[:n_features_to_select,:]
importances_.to_csv('../data/analysis/rft_%s_%s.csv'%(n_features_to_select,n_features_to_select_from),index=True,header=True)