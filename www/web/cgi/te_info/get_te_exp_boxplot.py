#!/usr/bin/python3
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
import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')


# Create the connection object
connection = MySQLdb.connect(
    user='www-data',
    passwd='www-data-passwd',
    host='127.0.0.1',
    port=3306,
    db='scARE'
)
form=cgi.FieldStorage()
name=form['Name'].value

cursor = connection.cursor()

cursor.execute(f"select * from  TE_EXP_BOXPLOT where TE='{name}' ORDER BY DATASET,DISEASE,CELL_TYPE ASC; ")

info=cursor.fetchall()
ret={}
labels={}
diseases=[]
if info:
    for row in info:
        _,cell,cell_n,dataset,disease,_,max_,min_,q1,median,q3= row
        if disease != 'Control':
            disease=dataset.split('_')[0]
            
        if all([x>0 for x in [max_,min_,q1,median,q3]]):
            if dataset not in ret:
                ret[dataset]=[]
                labels[dataset]=[]
                diseases=[]
            if disease not in diseases:
                ret[dataset].append({'data':[],'name':disease})
                labels[dataset].append([])
            diseases.append(disease)
            ret[dataset][-1]['data'].append([min_,q1,median,q3,max_])
            labels[dataset][-1].append(cell)
    print(json.dumps([ret,labels]))
else:
    print('ERROR: {name} not expressed in any dataset.')
