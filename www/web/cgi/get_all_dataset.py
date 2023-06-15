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

import config
# Create the connection object
connection = MySQLdb.connect(
    user=config.user,
    passwd=config.passwd,
    host=config.host,
    port=config.port,
    db=config.db
)

cursor = connection.cursor()

sql='select scARE_ID,DISEASE,METHODOLOGY,PROTOCOL,ACCESSION from DATASET_META'
cursor.execute(sql)
info=cursor.fetchall()


table_head='''<table id="ds_table" class="display stripe hover cell-border row-border order-column compact">\
    <thead><tr><th>scARE ID</th><th>Disease</th><th>Methodology</th><th>Protocol</th><th>Accession</th></tr></thead><tbody>{table_row}</tbody></table>'''
table_row=''
table_row_fmt='''<tr><td><a href='dataset_detail.html?Cate=Dataset&KW={scARE_ID}' target='_blank'>{scARE_ID}</a></td><td>{DISEASE}</td><td>{METHODOLOGY}</td><td>{PROTOCOL}</td><td>{ACCESSION}</td></tr>'''

for row in info:
    scARE_ID, DISEASE, METHODOLOGY,PROTOCOL,ACCESSION=row

    if ACCESSION.startswith('GSE'):
        ACCESSION=f'<a href="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={ACCESSION}" target="_blank">{ACCESSION}</a>'
    elif ACCESSION.startswith('syn'):
        ACCESSION=f'<a href="https://www.synapse.org/#!Synapse:{ACCESSION}" target="_blank">{ACCESSION}</a>'

    table_row+=table_row_fmt.format(scARE_ID=scARE_ID,DISEASE=DISEASE,METHODOLOGY=METHODOLOGY,PROTOCOL=PROTOCOL,ACCESSION=ACCESSION)

print(table_head.format(table_row=table_row))