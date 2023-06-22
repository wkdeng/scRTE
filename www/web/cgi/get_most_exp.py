#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
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
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')



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
    form=cgi.FieldStorage()
    cell=int(form['Cell'].value)
    number=int(form['Num'].value)
    condition=form['Condition'].value
    cells=['All','Ex','In','OPC','Oli','Ast','Mic','Endo','VLMC']
    cell=cells[cell]

    if cell not in ['All','Ex','In','Mic','Ast','OPC','Oli','VLMC']:
        raise Exception('Cell type not found.')
    if condition not in ['All','AD','PD','MS','Control']:
        raise Exception('Condition not found.')
    
    cursor,cnx=config.get_cursor()
    sql=f'select * from TE_EXP_BOXPLOT where '
    if not cell=='All':
        sql+=f"CELL_TYPE ='{cell}' and "

    sql+=f" DISEASE='{condition}'"
    sql+=f' Order by MEDIAN desc Limit {number};'
    cursor.execute(sql)
    info=cursor.fetchall()


    table_content = '''<table class="table table-striped" id='most_exp_table'>  <caption>{caption}</caption>\
    <thead><tr><th scope="col">TE</th><th scope="col">Dataset</th><th scope="col">Condition</th>\
    <th scope="col">Max</th><th scope="col">Q3</th><th scope="col">Median</th><th scope="col">Q1</th><th scope="col">Min</th></tr></thead><tbody>{table_row}</tbody></table>'''
    table_row = ''
    row_fmt = '''<tr><td><a href='te_info.html?Name={te}' target='_blank'>{te}</td><td><a href='dataset_detail.html?Cate=Dataset&KW={dataset}&Gene={te}&Cell=All' target='_blank'>{dataset}</a></td><td>{condition}</td><td>{max}</td><td>{Q3}</td><td>{Median}</td><td>{Q1}</td>\
    <td>{Min}</td></tr>'''

    colors=['#7cb5ec','#434348','#90ed7d','#f7a35c','#8085e9','#f15c80','#e4d354','#2b908f','#f45b5b']
    ret=[]
    ret_high=[{'name':'Most expressed TE','data':[]}]
    labels=[]
    i=0
    for row in info:
        _,cell,cell_n,dataset,disease,te,max_,min_,q1,median,q3= row
        if disease != 'Control':
            disease=dataset.split('_')[0]
        name=te+'/'+cell+'/'+disease+'/'+dataset
        ret_t={'x':[],'y':[],'name':[],'type':'box'}

        ret_t['x'].extend([name]*5)
        ret_t['y'].extend([max_,q3,median,q1,min_])
        ret_high[0]['data'].append({'x':len(labels),'low':min_,'q1':q1,'median':median,'q3':q3,'high':max_,'fillColor':colors[i]})
        labels.append(name)
        table_row+=row_fmt.format(te=te,dataset=dataset,condition=disease,max=max_,Q3=q3,Median=median,Q1=q1,Min=min_)
        ret.append(ret_t)
        i+=1
        if i==9:
            i=0
    table_content = table_content.format(caption=f'Top {number} most expressed TE in {cell} cells with condition {disease}',table_row=table_row)
    print(json.dumps([[ret_high,labels],table_content]))
except Exception as e:
      print('An error occurred when fetching information.')