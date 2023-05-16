#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-15 22:48:37
 # @modify date 2023-05-15 22:48:37
 # @desc [description]
#############################

import cgitb
import pandas as pd
import cgi
import json
import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

# Create the connection object
connection = MySQLdb.connect(
    user='www-data',
    passwd='www-data-passwd',
    host='127.0.0.1',
    port=3306,
    db='scARE'
)

cursor = connection.cursor()

sql='select scARE_ID,DISEASE,CELL_TYPE,METHODOLOGY from DATASET_META'
cursor.execute(sql)
info=cursor.fetchall()


table_head='''<table id="ds_table" class="display stripe hover cell-border row-border order-column compact">\
    <thead><tr><th>scARE ID</th><th>Disease</th><th>Cell Types</th><th>Methodology</th></tr></thead><tbody>{table_row}</tbody></table>'''
table_row=''
table_row_fmt='''<tr><td><a href='dataset_detail.html?Cate=Dataset&KW={scARE_ID}' target='_blank'>{scARE_ID}</a></td><td>{DISEASE}</td><td>{CELL_TYPE}\
    </td><td>{METHODOLOGY}</td></tr>'''

for row in info:
    scARE_ID, DISEASE, CELL_TYPE, METHODOLOGY=row
    CELL_TYPE='; '.join(set(CELL_TYPE.split(';')))
    table_row+=table_row_fmt.format(scARE_ID=scARE_ID, DISEASE=DISEASE, CELL_TYPE=CELL_TYPE, METHODOLOGY=METHODOLOGY)

print(table_head.format(table_row=table_row))