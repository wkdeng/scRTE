#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
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
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')


form = cgi.FieldStorage()
gene=form['Gene'].value
dataset=form['Dataset'].value


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
    cursor,cnx=config.get_cursor()
    cursor.execute(f"select TABLE_ID from GENE_DICT WHERE GENE='{gene}' ")
    table_id=cursor.fetchone()[0]
    cursor.execute(f"select CELL, UMAP_1, UMAP_2, `{gene}` from CELL_EXP_{table_id} where scARE_ID='{dataset}';")
    info=cursor.fetchall()

    info=pd.DataFrame(info,columns=['CELL','x','y','value'])
    print(json.dumps(list(info.transpose().to_dict().values())))
except Exception as e:
      print('An error occurred when fetching information.')