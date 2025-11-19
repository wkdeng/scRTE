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
Dataset=form['Dataset'].value


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
    cursor.execute(f"select CELL, CELL_TYPE, UMAP_1, UMAP_2 from DATA_CELLUMAP WHERE scARE_ID = '{Dataset}' ")
    info=cursor.fetchall()


    info=pd.DataFrame(info,columns=['CELL','CELL_TYPE','UMAP_1','UMAP_2'])
    # info.index=info['CELL']
    # info=info.drop(columns=['CELL'])
    print(json.dumps(list(info.transpose().to_dict().values())))
except Exception as e:
      print('An error occurred when fetching information.')