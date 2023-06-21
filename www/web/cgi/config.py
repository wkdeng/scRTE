import json
import os
import mysql.connector

current_folder=os.path.abspath('.')
if current_folder.endswith('te_info'):
    config_path='../config.json'
else:
    config_path='config.json'
host,user,passwd,port,db=json.load(fp=open(config_path,'r'))

def get_cursor():
    cnx=mysql.connector.connect(user=user,password=passwd,host=host,port=port,database=db)
    cursor=cnx.cursor()
    return cursor,cnx
