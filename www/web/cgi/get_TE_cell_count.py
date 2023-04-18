#!/usr/bin/python3
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
import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')


form = cgi.FieldStorage()
gene=form['Name'].value


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

sql=f"select DATA_CELLUMAP.disease, DATA_CELLUMAP.cell_type, COUNT(*) AS number_of_cells FROM DATA_CELLUMAP INNER JOIN CELL_EXP_{table_id} ON DATA_CELLUMAP.CELL=CELL_EXP_7.CELL where CELL_EXP_{table_id}.{gene} >0 GROUP by disease, cell_type; "
cursor.execute(sql)
info=cursor.fetchall()

info=pd.DataFrame(info,columns=['disease','cell_type','number_of_cells'])
print(json.dumps(list(info.transpose().to_dict().values())))