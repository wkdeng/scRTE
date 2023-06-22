#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-18 10:15:15
 # @modify date 2023-04-18 10:15:15
 # @desc [description]
#############################
import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')


form = cgi.FieldStorage()
kw=form['KW'].value
cate=form['Cate'].value

import config
# Create the connection object
# connection = MySQLdb.connect(
#     user=config.user,
#     passwd=config.passwd,
#     host=config.host,
#     port=config.port,
#     db=config.db
# )

try:
    cursor,cnx=config.get_cursor()
    
    if cate=='TE':
        # cursor = connection.cursor()
        cursor.execute(f"select TABLE_ID from GENE_DICT WHERE GENE='{kw}' ")
        table_id=cursor.fetchone()[0]

        sql=f"select DATA_CELLUMAP.disease, DATA_CELLUMAP.cell_type, COUNT(*) AS number_of_cells FROM DATA_CELLUMAP INNER JOIN CELL_EXP_{table_id} ON DATA_CELLUMAP.CELL=CELL_EXP_{table_id}.CELL where CELL_EXP_{table_id}.{kw} >0 GROUP by disease, cell_type; "
        cursor.execute(sql)
        info=cursor.fetchall()

        info=pd.DataFrame(info,columns=['disease','cell_type','number_of_cells'])
        print(json.dumps(list(info.transpose().to_dict().values())))
    elif cate=='Dataset':
        # cursor = connection.cursor()
        # sql=f"select DATA_CELLUMAP.disease, DATA_CELLUMAP.cell_type, COUNT(*) AS number_of_cells FROM DATA_CELLUMAP JOIN SAMPLE2DATASET ON DATA_CELLUMAP.DATASET = SAMPLE2DATASET.SAMPLE_ID WHERE SAMPLE2DATASET.scARE_ID = '{kw}' GROUP by disease, cell_type; "
        sql=f"select disease, cell_type, COUNT(*) AS number_of_cells FROM DATA_CELLUMAP where scARE_ID = '{kw}' GROUP by disease, cell_type; "
        cursor.execute(sql)
        info=cursor.fetchall()

        info=pd.DataFrame(info,columns=['disease','cell_type','number_of_cells'])
        print(json.dumps(list(info.transpose().to_dict().values())))
    elif cate=='Cell':
        # cursor = connection.cursor()
        # sql=f"select DATA_CELLUMAP.disease, DATA_CELLUMAP.cell_type, COUNT(*) AS number_of_cells FROM DATA_CELLUMAP JOIN SAMPLE2DATASET ON DATA_CELLUMAP.DATASET = SAMPLE2DATASET.SAMPLE_ID WHERE SAMPLE2DATASET.scARE_ID = '{kw}' GROUP by disease, cell_type; "
        sql=f"select disease, COUNT(*) AS number_of_cells FROM DATA_CELLUMAP where cell_type = '{kw}' GROUP by disease; "
        cursor.execute(sql)
        info=cursor.fetchall()

        info=pd.DataFrame(info,columns=['disease','number_of_cells'])
        for disease in ['AD','PD','MS','Control']:
            if disease not in list(info['disease']):
                info=info.append({'disease':disease,'number_of_cells':0},ignore_index=True)
        disease_cate=['AD','PD','MS','Control']
        info['disease']=pd.Categorical(info['disease'],categories=disease_cate,ordered=True)
        info=info.sort_values(by=['disease'])
        info.columns=['name','y']
        print('[{values}]'.format(values=','.join(info['y'].astype(str).values.tolist())))
        # print(json.dumps(list(info.transpose().to_dict().values())))
    elif cate=='Cell_Dataset':
        # cursor = connection.cursor()
        sql=f" select scARE_ID, COUNT(*)  AS number_of_cells from DATA_CELLUMAP where CELL_TYPE='{kw}' group by scARE_ID;"
        cursor.execute(sql)
        info=cursor.fetchall()

        info=pd.DataFrame(info,columns=['name','y'])

        print(json.dumps(list(info.transpose().to_dict().values())))
    elif cate=='Cell_TE':
        # cursor = connection.cursor()
        if kw=='In':
            kw='`In`'
        sql=f" select TE,{kw} from FAM_CELL_COUNT;"
        cursor.execute(sql)
        info=cursor.fetchall()
        info=pd.DataFrame(info,columns=['name','y'])
        info=info.loc[info.iloc[:,1]>0,:]
        info['drilldown']=info['name']

        drilldown=[]
        for te_fam in info['name']:
            sql=f" select TE, {kw} from SUBFAM_CELL_COUNT where TE_FAM='{te_fam}';"
            cursor.execute(sql)
            info2=cursor.fetchall()
            info2=pd.DataFrame(info2,columns=['name','y'])
            drilldown.append({'name':te_fam,'type':'column','id':te_fam,'data':list(info2.transpose().to_dict().values())})
        ret=[list(info.transpose().to_dict().values()),drilldown]
        print(json.dumps(ret))
        # print([json.dumps(),json.dumps(drilldown)])
    else:
        print('Wrong categoery!')
except Exception as e:
        print('An error occurred when fetching information.')