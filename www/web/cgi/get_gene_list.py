#!/usr/bin/python3
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
import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

import config
# Create the connection object
connection = MySQLdb.connect(
    user=config.user,
    passwd=config.passwd,
    host=config.host,
    port=config.port,
    db=config.db
)

cursor=connection.cursor()
cursor.execute("select GENE from  GENE_DICT where TABLE_ID=0 ORDER BY GENE ASC; ")
info=cursor.fetchall()
print(json.dumps([x[0] for x in info]))