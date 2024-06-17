import pandas as pd
import numpy as np
import sys
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score,StratifiedKFold
from sklearn.ensemble import RandomForestClassifier


n_features_to_select=int(sys.argv[1])
cell_exp=pd.read_csv('../data/analysis/combined_exp1460.txt',sep='\t')
sfg_umap=pd.read_csv('../data/all_datasets/AD_HS_00003.1.cell_umap.txt',sep='\t',index_col=0)
sfg_umap=sfg_umap.loc[sfg_umap['predicted.celltype']=='Ex',:]
factors=pd.factorize(sfg_umap['Diagnosis'])
labels=factors[0]

rfe = RFE(estimator=RandomForestClassifier(n_estimators=100,random_state=42), n_features_to_select=n_features_to_select)
model = RandomForestClassifier(n_estimators=100,random_state=42)
pipeline = Pipeline(steps=[('s',rfe),('m',model)])
cv = StratifiedKFold(n_splits=10, shuffle=True,random_state=42)
n_scores = cross_val_score(pipeline, cell_exp.to_numpy(), labels, scoring='accuracy', cv=cv, n_jobs=100, error_score='raise')
print('Feature to select: %s'%n_features_to_select)
print('Accuracy: %.3f (%.3f)' % (np.mean(n_scores), np.std(n_scores)))
