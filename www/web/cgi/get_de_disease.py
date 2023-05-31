#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-30 12:06:29
 # @modify date 2023-05-30 12:06:29
 # @desc [description]
#############################


import cgitb
import pandas as pd
import cgi
import json
import MySQLdb
import random
import numpy
from scipy import stats
from statsmodels.stats.multitest import multipletests
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

form=cgi.FieldStorage()
cell=['Ex','In','OPC','Oli','Ast','Mic','Endo','VLMC'][int(form['Cell'].value)-1]
disease=form['Disease'].value

import config
# Create the connection object
connection = MySQLdb.connect(
    user=config.user,
    passwd=config.passwd,
    host=config.host,
    port=config.port,
    db=config.db
)

cursor = connection.cursor()

sql=f"select * from TE_EXP_BOXPLOT where CELL_TYPE ='{cell}' and (DISEASE='{disease}' or DISEASE='Control');"
cursor.execute(sql)
info=cursor.fetchall()
info=pd.DataFrame(info)
info.columns=['ID','CELL_TYPE','CELL_NUM','DATASET','DISEASE','TE','MAX','MIN','Q1','MEDIAN','Q3']

disease_set=info[info['DISEASE']!='Control']
disease_set=disease_set[disease_set['MEDIAN']>3]
control_set=info[info['DISEASE']=='Control']
datasets=disease_set['DATASET'].unique()
# print(info.to_string())
ret=[]
for dataset in datasets:
    data=disease_set[disease_set['DATASET']==dataset]
    tes=data['TE'].unique()
    for te in tes:
        disease_q1,disease_median,disease_q3=numpy.exp(data[data['TE']==te][['Q1','MEDIAN','Q3']].values)[0]
        control_q1,control_median,control_q3=numpy.exp(control_set[(control_set['TE']==te) & (control_set['DATASET']==dataset)][['Q1','MEDIAN','Q3']].values)[0]

        fc=numpy.log2(disease_median/control_median)
        disease_scale=(disease_q3-disease_q1)/2
        control_scale=(control_q3-control_q1)/2
        disease_vs=numpy.random.normal(disease_median,disease_scale,100)
        control_vs=numpy.random.normal(control_median,control_scale,100)
        try:
            pval=stats.wilcoxon(disease_vs,control_vs)[1]
        except:
            pval=1
        ret.append([te,dataset,f'{disease} v.s. Control',cell,numpy.log(disease_median),numpy.log(control_median),fc,pval])
ret=pd.DataFrame(ret)
ret.columns=['TE','Dataset','Comparison','Cell','Disease_m','Control_m','FC','Pval']
ret['Qval']=multipletests(ret['Pval'],method='fdr_bh')[1]
ret=ret[ret['Qval']<0.5]

table_content = '''<table class="table table-striped" id='disease_de_table'>  <caption>{caption}</caption>\
<thead><tr><th scope="col">TE</th>\
<th scope="col">Dataset</th>\
<th scope="col">Comparison</th>\
<th scope="col">Cell</th>\
<th scope="col">Disease median</th>\
<th scope="col">Control median</th>\
<th scope="col">Log2(FC)</th>\
<th scope="col">Pval</th>\
<th scope="col">P_adjusted</th>\
</tr></thead><tbody>{table_row}</tbody></table>'''
table_row = ''
row_fmt = '''<tr><td><a href='te_info.html?Name={te}' target='_blank'>{te}</td>\
<td>{dataset}</td>\
<td>{comparison}</td>\
<td>{cell}</td>\
<td>{disease_median}</td>\
<td>{control_median}</td>\
<td>{fc}</td>\
<td>{pval}</td>\
<td>{qval}</td></tr>'''

ret=ret.sort_values(by=['Qval'])
for i in range(len(ret)):
    te,dataset,comparison,_,disease_median,control_median,fc,pval,qval = ret.iloc[i,:]
    disease_median='{:.2f}'.format(disease_median)
    control_median='{:.2f}'.format(control_median)
    fc='{:.4f}'.format(fc)
    pval='{:.2e}'.format(pval)
    qval='{:.2e}'.format(qval)
    table_row += row_fmt.format(te=te,dataset=dataset,comparison=comparison,cell=cell,disease_median=disease_median,control_median=control_median,fc=fc,pval=pval,qval=qval)
print(table_content.format(caption='Most differentially expressed TE',table_row=table_row))