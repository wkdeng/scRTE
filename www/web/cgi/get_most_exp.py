#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-27 09:44:13
 # @modify date 2023-05-27 09:44:13
 # @desc [description]
#############################
import cgitb
import pandas as pd
import cgi
import json
import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

form=cgi.FieldStorage()
cell=int(form['Cell'].value)
number=int(form['Num'].value)
condition=form['Condition'].value
cells=['All','Ex','In','OPC','Oli','Ast','Mic','Endo','VLMC']
cell=cells[cell]

import config
# Create the connection object
connection = MySQLdb.connect(
    user=config.user,
    passwd=config.passwd,
    host=config.host,
    port=config.port,
    db=config.db
)

sql=f'select * from TE_EXP_BOXPLOT where '
if not cell=='All':
    sql+=f"CELL_TYPE ='{cell}'"

sql+=f" and DISEASE='{condition}'"

cursor = connection.cursor()
sql+=f' Order by MEDIAN desc Limit {number};'
cursor.execute(sql)
info=cursor.fetchall()


table_content = '''<table class="table table-striped" id='most_exp_table'>  <caption>{caption}</caption>\
<thead><tr><th scope="col">TE</th><th scope="col">Dataset</th><th scope="col">Condition</th>\
<th scope="col">Max</th><th scope="col">Q3</th><th scope="col">Median</th><th scope="col">Q1</th><th scope="col">Min</th></tr></thead><tbody>{table_row}</tbody></table>'''
table_row = ''
row_fmt = '''<tr><td><a href='te_info.html?Name={te}' target='_blank'>{te}</td><td>{dataset}</td><td>{condition}</td><td>{max}</td><td>{Q3}</td><td>{Median}</td><td>{Q1}</td>\
<td>{Min}</td></tr>'''

ret=[]
for row in info:
    _,cell,cell_n,dataset,disease,te,max_,min_,q1,median,q3= row
    if disease != 'Control':
        disease=dataset.split('_')[0]
    name=te+'/'+cell+'/'+disease+'/'+dataset
    ret_t={'x':[],'y':[],'name':[],'type':'box'}

    ret_t['x'].extend([name]*5)
    ret_t['y'].extend([max_,q3,median,q1,min_])
    # ret_t['marker']['color']=
    table_row+=row_fmt.format(te=te,dataset=dataset,condition=disease,max=max_,Q3=q3,Median=median,Q1=q1,Min=min_)
    ret.append(ret_t)
table_content = table_content.format(caption=f'Top {number} most expressed TE in {cell} cells with condition {disease}',table_row=table_row)
print(json.dumps([ret,table_content]))