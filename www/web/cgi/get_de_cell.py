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
cell1=['Ex','In','OPC','Oli','Ast','Mic','Endo','VLMC'][int(form['Cell1'].value)]
cell2=['Ex','In','OPC','Oli','Ast','Mic','Endo','VLMC'][int(form['Cell2'].value)]
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

sql=f"select * from TE_EXP_BOXPLOT where (CELL_TYPE ='{cell1}' or CELL_TYPE='{cell2}') and DISEASE='{disease}' ;"
cursor.execute(sql)
info=cursor.fetchall()
info=pd.DataFrame(info)
info.columns=['ID','CELL_TYPE','CELL_NUM','DATASET','DISEASE','TE','MAX','MIN','Q1','MEDIAN','Q3']

cell1_set=info[info['CELL_TYPE']==cell1]
cell1_set=cell1_set[cell1_set['MEDIAN']>3]

cell2_set=info[info['CELL_TYPE']==cell2]


datasets=cell1_set['DATASET'].unique()
# print(info.to_string())
ret=[]
for dataset in datasets:
    data=cell1_set[cell1_set['DATASET']==dataset]
    tes=data['TE'].unique()
    for te in tes:
        cell1_q1,cell1_median,cell1_q3=numpy.exp(data[data['TE']==te][['Q1','MEDIAN','Q3']].values)[0]
        if cell2 in cell2_set[(cell2_set['DATASET']==dataset) & (cell2_set['TE']==te)]['CELL_TYPE'].unique():
            cell2_q1,cell2_median,cell2_q3=numpy.exp(cell2_set[(cell2_set['TE']==te) & (cell2_set['DATASET']==dataset)][['Q1','MEDIAN','Q3']].values)[0]

            fc=numpy.log2(cell1_median/cell2_median)
            cell1_scale=(cell1_q3-cell1_q3)/2
            cell2_scale=(cell2_q3-cell2_q1)/2
            cell1_vs=numpy.random.normal(cell1_median,cell1_scale,100)
            cell2_vs=numpy.random.normal(cell2_median,cell2_scale,100)
            try:
                pval=stats.wilcoxon(cell1_vs,cell2_vs)[1]
            except:
                pval=1
            ret.append([te,dataset,cell1,cell2,disease,numpy.log(cell1_median),numpy.log(cell2_median),fc,pval])
        else:
            print('no')
ret=pd.DataFrame(ret)
ret.columns=['TE','Dataset','Cell1','Cell2','Disease','Cell1 median','Cell2 median','FC','Pval']
ret['Qval']=multipletests(ret['Pval'],method='fdr_bh')[1]
ret=ret[ret['Qval']<0.5]

table_content = '''<table class="table table-striped" id='cell_de_table'>  <caption>{caption}</caption>\
<thead><tr><th scope="col">TE</th>\
<th scope="col">Dataset</th>\
<th scope="col">Cell1</th>\
<th scope="col">Cell2</th>\
<th scope="col">Disease</th>\
<th scope="col">Cell1 median</th>\
<th scope="col">Cell2 median</th>\
<th scope="col">Log2(FC)</th>\
<th scope="col">Pval</th>\
<th scope="col">P_adjusted</th>\
</tr></thead><tbody>{table_row}</tbody></table>'''
table_row = ''
row_fmt = '''<tr><td><a href='te_info.html?Name={te}' target='_blank'>{te}</td>\
<td>{dataset}</td>\
<td>{cell1}</td>\
<td>{cell2}</td>\
<td>{disease}</td>\
<td>{cell1_median}</td>\
<td>{cell2_median}</td>\
<td>{fc}</td>\
<td>{pval}</td>\
<td>{qval}</td></tr>'''

ret=ret.sort_values(by=['Qval'])
for i in range(len(ret)):
    te,dataset,_,_,disease,cell1_median,cell2_median,fc,pval,qval = ret.iloc[i,:]
    cell1_median='{:.2f}'.format(cell1_median)
    cell2_median='{:.2f}'.format(cell2_median)
    fc='{:.4f}'.format(fc)
    pval='{:.2e}'.format(pval)
    qval='{:.2e}'.format(qval)
    table_row += row_fmt.format(te=te,dataset=dataset,cell1=cell1,cell2=cell2,disease=disease,cell1_median=cell1_median,cell2_median=cell2_median,fc=fc,pval=pval,qval=qval)
print(table_content.format(caption='Most differentially expressed TE',table_row=table_row))