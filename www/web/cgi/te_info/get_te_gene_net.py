#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-07 16:26:23
 # @modify date 2023-05-07 16:26:23
 # @desc [description]
#############################
import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb
import urllib.parse
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

import sys
sys.path.append('../')
import config
form=cgi.FieldStorage()
name=form['Name'].value
degree=form['Degree'].value

## Create the connection object
# connection = MySQLdb.connect(
#     user=config.user,
#     passwd=config.passwd,
#     host=config.host,
#     port=config.port,
#     db=config.db
# )
# cursor = connection.cursor()
# sql=f"select D{degree} from TE_NET WHERE NAME = '{name}'"
# cursor.execute(sql)
# res=cursor.fetchone()
# res=json.loads(res[0])

sql=f"select D{degree} from TE_NET WHERE NAME = '{name}'"
info,cnx=config.get_cursor()
info.execute(sql)
res=json.loads(info[0])


# nodes=[]
# links=[]
# color=["#a6cee3", "#fb9a99"]
# for item in res['nodes']:
#     nodes.append({'id':item['id'],'color':color[item['group']]})
# for item in res['links']:
#     links.append([item['source'],item['target']])

print(json.dumps(res))
# print('')s