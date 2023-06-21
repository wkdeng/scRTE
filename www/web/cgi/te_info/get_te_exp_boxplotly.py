#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-23 09:28:05
 # @modify date 2023-05-23 09:28:05
 # @desc [description]
#############################

import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')


import sys
sys.path.append('../')
import config
form=cgi.FieldStorage()
name=form['Name'].value


# # Create the connection object
# connection = MySQLdb.connect(
#     user=config.user,
#     passwd=config.passwd,
#     host=config.host,
#     port=config.port,
#     db=config.db
# )
# cursor = connection.cursor()
# cursor.execute(f"select * from  TE_EXP_BOXPLOT where TE='{name}' ORDER BY DATASET,DISEASE,CELL_TYPE ASC; ")
# info=cursor.fetchall()

sql=f"select * from  TE_EXP_BOXPLOT where TE='{name}' ORDER BY DATASET,DISEASE,CELL_TYPE ASC; "
cursor,cnx=config.get_cursor()
cursor.execute(sql)
info=cursor.fetchall()

colors=["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
ret={}
diseases=[]
if info:
    for row in info:
        _,cell,cell_n,dataset,disease,_,max_,min_,q1,median,q3= row
        if disease != 'Control':
            disease=dataset.split('_')[0]
            
        if all([x>0 for x in [max_,min_,q1,median,q3]]):
            if dataset not in ret:
                ret[dataset]=[]
                # labels[dataset]=[]
                diseases=[]
            if disease not in diseases:
                ret[dataset].append({'y':[],'x':[],'name':disease,'type':'box','maker':{'color':colors[1] if disease=='Control' else colors[0]}})
                # labels[dataset].append([])
                diseases.append(disease)
            ret[dataset][-1]['y'].extend([min_,q1,median,q3,max_])
            ret[dataset][-1]['x'].extend([cell]*5)
            # labels[dataset][-1].append(cell)
    print(json.dumps(ret))
else:
    print('{"NO_EXP":"No expression data for this TE."}')
