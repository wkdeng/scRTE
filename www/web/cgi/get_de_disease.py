#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
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
# import MySQLdb
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
# # Create the connection object
# connection = MySQLdb.connect(
#     user=config.user,
#     passwd=config.passwd,
#     host=config.host,
#     port=config.port,
#     db=config.db
# )
# cursor = connection.cursor()
try:
    if cell not in ['All','Ex','In','Mic','Ast','OPC','Oli','VLMC']:
        raise Exception('Cell type not found.')
    if disease not in ['All','AD','PD','MS','Control']:
        raise Exception('Disease not found.')

    cursor,cnx=config.get_cursor()
    # sql=f"select * from TE_EXP_BOXPLOT where CELL_TYPE ='{cell}' and (DISEASE='{disease}' or DISEASE='Control');"
    # cursor.execute(sql)
    # info=cursor.fetchall()
    # info=pd.DataFrame(info)
    # info.columns=['ID','CELL_TYPE','CELL_NUM','DATASET','DISEASE','TE','MAX','MIN','Q1','MEDIAN','Q3']

    # disease_set=info[info['DISEASE']!='Control']
    # disease_set=disease_set[disease_set['MEDIAN']>3]
    # control_set=info[info['DISEASE']=='Control']
    # datasets=disease_set['DATASET'].unique()
    # # print(info.to_string())
    # ret=[]
    # for dataset in datasets:
    #     data=disease_set[disease_set['DATASET']==dataset]
    #     tes=data['TE'].unique()
    #     for te in tes:
    #         disease_q1,disease_median,disease_q3=numpy.exp(data[data['TE']==te][['Q1','MEDIAN','Q3']].values)[0]
    #         control_q1,control_median,control_q3=numpy.exp(control_set[(control_set['TE']==te) & (control_set['DATASET']==dataset)][['Q1','MEDIAN','Q3']].values)[0]

    #         fc=numpy.log2(disease_median/control_median)
    #         disease_scale=(disease_q3-disease_q1)/2
    #         control_scale=(control_q3-control_q1)/2
    #         disease_vs=numpy.random.normal(disease_median,disease_scale,100)
    #         control_vs=numpy.random.normal(control_median,control_scale,100)
    #         try:
    #             pval=stats.wilcoxon(disease_vs,control_vs)[1]
    #         except:
    #             pval=1
    #         ret.append([te,dataset,f'{disease} v.s. Control',cell,numpy.log(disease_median),numpy.log(control_median),fc,pval])
    # ret=pd.DataFrame(ret)
    # ret.columns=['TE','Dataset','Comparison','Cell','Disease_m','Control_m','FC','Pval']


    compare='{} v.s. {}'.format(disease,'Control')
    sql="select * from EXP_DE where COMPARISON = '{}' and `CELL`='{}';".format(compare,cell)
    cursor.execute(sql)
    ret=cursor.fetchall()
    ret=pd.DataFrame(ret)
    ret.columns=['TE','Comparison','Dataset','Cell','Disease','Cell1 mean','Cell2 mean','FC','Pval','PoE1','PoE2']
    ret['Qval']=multipletests(ret['Pval'],method='fdr_bh')[1]
    ret=ret[ret['Qval']<0.5]

    table_content = '''<table class="table table-striped" id='disease_de_table'>  <caption>{caption}</caption>\
    <thead><tr><th scope="col">TE</th>\
    <th scope="col">Dataset</th>\
    <th scope="col">Cell</th>\
    <th scope="col">Disease median</th>\
    <th scope="col">Control median</th>\
    <th scope="col">Disease PoCE(%)</th>\
    <th scope="col">Control PoCE(%)</th>\
    <th scope="col">Log2(FC)</th>\
    <th scope="col">Pval</th>\
    <th scope="col">P_adj</th>\
    </tr></thead><tbody>{table_row}</tbody></table>'''
    table_row = ''
    row_fmt = '''<tr><td><a href='te_info.html?Name={te}' target='_blank'>{te}</td>\
    <td><a href='dataset_detail.html?Cate=Dataset&KW={dataset}&Gene={te}&Cell=All' target='_blank'>{dataset}</a></td>\
    <td>{cell}</td>\
    <td>{disease_median}</td>\
    <td>{control_median}</td>\
    <td>{poe1}</td>\
    <td>{poe2}</td>\
    <td>{fc}</td>\
    <td>{pval}</td>\
    <td>{qval}</td></tr>'''

    ret=ret.sort_values(by=['Qval'])
    for i in range(len(ret)):
        te,comparison,dataset,cell,_,disease_median,control_median,fc,pval,poe1,poe2,qval = ret.iloc[i,:]
        disease_median='{:.2f}'.format(disease_median) if disease_median>0.01 else '{:.2e}'.format(disease_median)
        control_median='{:.2f}'.format(control_median) if control_median>0.01 else '{:.2e}'.format(control_median)
        poe1='{:.2f}'.format(poe1*100.0) if poe1>0.0001 else '{:.2e}'.format(poe1*100.0)
        poe2='{:.2f}'.format(poe2*100.0) if poe2>0.0001 else '{:.2e}'.format(poe2*100.0)
        fc='{:.4f}'.format(fc)
        pval='{:.2e}'.format(pval)
        qval='{:.2e}'.format(qval)
        table_row += row_fmt.format(te=te,dataset=dataset,poe1=poe1,poe2=poe2,cell=cell,disease_median=disease_median,control_median=control_median,fc=fc,pval=pval,qval=qval)
    print(table_content.format(caption='Most differentially expressed TE',table_row=table_row))
except Exception as e:
      print('An error occurred when fetching information.')
