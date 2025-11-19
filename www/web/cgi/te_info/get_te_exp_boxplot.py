#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-22 22:59:04
 # @modify date 2023-05-22 22:59:04
 # @desc [description]
#############################

import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb

import sys
sys.path.append('../')
import config
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')
form=cgi.FieldStorage()
name=form['Name'].value

sql=f"select * from  TE_EXP_BOXPLOT where TE='{name}' ORDER BY DATASET,DISEASE,CELL_TYPE ASC; "
cursor,cnx=config.get_cursor()
cursor.execute(sql)
info=cursor.fetchall()

ret={}
ret_high={}
labels={} 
diseases=[]

if info:
    for row in info:
        _,cell,cell_n,dataset,disease,_,max_,min_,q1,median,q3= row
        if disease != 'Control':
            disease=dataset.split('_')[0]
        if all([x>=0 for x in [max_,min_,q1,median,q3]]):
            if dataset not in ret_high:
                labels[dataset]=[]
                diseases=[]
                ret_high[dataset]=[]
            if disease not in diseases:
                ret_high[dataset].append({'data':[],'name':disease,'color':'#7cb5ec' if disease=='Control' else '#f7a35c','fillColor':'#99caf7' if disease=='Control' else '#fac89d'})
            diseases.append(disease)
            if cell not in labels[dataset]:
                labels[dataset].append(cell)
            ret_high[dataset][-1]['data'].append({'x':labels[dataset].index(cell),'low':min_,'q1':q1,'median':median,'q3':q3,'high':max_})

    print(json.dumps([ret_high,labels]))
else:
    print(json.dumps(['No data']))
