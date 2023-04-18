#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-14 14:57:27
 # @modify date 2023-04-14 14:57:27
 # @desc [description]
#############################
import cgitb
import pandas as pd
import cgi
import json
import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')


form = cgi.FieldStorage()
gene=form['Gene'].value


# Create the connection object
connection = MySQLdb.connect(
    user='www-data',
    passwd='www-data-passwd',
    host='127.0.0.1',
    port=3306,
    db='scARE'
)

cursor = connection.cursor()

cursor.execute(f"select TABLE_ID from GENE_DICT WHERE GENE='{gene}' ")
table_id=cursor.fetchone()[0]
cursor.execute(f"select CELL, UMAP_1, UMAP_2, `{gene}` from CELL_EXP_{table_id} ")
info=cursor.fetchall()

info=pd.DataFrame(info,columns=['CELL','x','y','value'])
print(json.dumps(list(info.transpose().to_dict().values())))