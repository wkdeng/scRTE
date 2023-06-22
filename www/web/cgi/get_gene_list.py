#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-06-02 11:34:03
 # @modify date 2023-06-02 11:34:03
 # @desc [description]
#############################

import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

# import config
# # # Create the connection object
# # connection = MySQLdb.connect(
# #     user=config.user,
# #     passwd=config.passwd,
# #     host=config.host,
# #     port=config.port,
# #     db=config.db
# # )
# # cursor=connection.cursor()

form=cgi.FieldStorage()
dataset=form['Dataset'].value

# cursor,cnx=config.get_cursor()
# cursor.execute(f"select LIST from  GENE_LIST where DATASET='{dataset}'")
# info=cursor.fetchone()
# print(info[0])
# print(json.dumps(info[0].split(',')))
with open(f'../data/{dataset}.txt','r') as f:
    print(json.dumps(f.readline().split(',')))