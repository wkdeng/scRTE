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
    cursor.execute(f"select scARE_ID from DATASET_META; ")

    info=cursor.fetchall()

    for dataset in info:
        dataset=dataset[0]
        print(f'<iframe width="100%" height="500px" src="dataset_detail.html?Cate=Dataset&KW={dataset}&CL=T"></iframe>')
except Exception as e:
      print('An error occurred when fetching information.')