#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-01 16:24:12
 # @modify date 2023-05-01 16:24:12
 # @desc [description]
#############################

import cgitb
import pandas as pd
import cgi
import json
import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

form=cgi.FieldStorage()
dataset=form['KW'].value

# Create the connection object
connection = MySQLdb.connect(
    user='www-data',
    passwd='www-data-passwd',
    host='127.0.0.1',
    port=3306,
    db='scARE'
)

cursor = connection.cursor()
sql=f'select * from DATASET_META where scARE_ID="{dataset}";'

cursor.execute(sql)
info=cursor.fetchone()

dataset,title,sampleN,_,disease,brain_region,stage,cell_types,acc,method,protocol,gender,age,sample_acc=info
brain_region='; '.join(set(brain_region.split(';')))
sample_acc=sample_acc.split(';')
cell_types=cell_types.replace(';','; ')
age=age.replace(';','; ')
stage=stage.replace(';','; ')

if acc.startswith('GSE'):
    acc=f'<a href="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={acc}" target="_blank">{acc}</a>'
elif acc.startswith('syn'):
    acc=f'<a href="https://www.synapse.org/#!Synapse:{acc}" target="_blank">{acc}</a>'

if sample_acc[0].startswith('SRR'):
    sample_acc=[f'<a href="https://trace.ncbi.nlm.nih.gov/Traces/sra/?run={i}" target="_blank">{i}</a>' for i in sample_acc]
elif sample_acc[0].startswith('syn'):
    sample_acc=[f'<a href="https://www.synapse.org/#!Synapse:{i}" target="_blank">{i}</a>' for i in sample_acc]

sample_acc='; '.join(sample_acc)
## basic row
basic_row=f'''
<ul>
<li>Title: {title}</li>
<li>Brain region: {brain_region}</li>
<li>Sample #: {sampleN}</li>
<li>Cell types: {cell_types}</li>
<li>Disease: {disease}</li>
<li>Protocol: {protocol}</li>
<li>Methodology: {method}</li>
<li>Accession: {acc}</li>
<li>Gender: {gender}</li>
<li>Age: {age}</li>
<li>Stage: {stage}</li>
<li>Sample accession: {sample_acc}</li>
</ul>
'''
table_content=f'<table><thead>{dataset}</thead><tr>{basic_row}</tr></table>'

print(table_content)