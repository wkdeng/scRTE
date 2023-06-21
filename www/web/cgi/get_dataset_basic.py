#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
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
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

try:
    form=cgi.FieldStorage()
    dataset=form['KW'].value

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

    cursor,cnx=config.get_cursor()
    sql=f'select * from DATASET_META where scARE_ID="{dataset}";'

    cursor.execute(sql)
    info=cursor.fetchone()

    dataset,title,sampleN,_,disease,brain_region,stage,cell_types,acc,method,protocol,gender,age,sample_acc,citation=info
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
    elif sample_acc[0].startswith('GSM'):
        sample_acc=[f'<a href="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={i}" target="_blank">{i}</a>' for i in sample_acc]

    sample_acc='; '.join(sample_acc)
    ## basic row
    basic_row='''
    <div class="row mb-3">
    <span class="col-md-4 {2}"><strong>{0}:</strong></span>
    <span class="col-md-8 {2}" style="word-wrap: break-word;">{1}</span>
    </div>
    '''
    ret=""
    ret+=basic_row.format('scARE ID',dataset,'bg-light')
    ret+=basic_row.format('Title',title,'')
    ret+=basic_row.format('Brain region',brain_region,'bg-light')
    ret+=basic_row.format('Sample #',sampleN,'')
    ret+=basic_row.format('Cell types',cell_types,'bg-light')
    ret+=basic_row.format('Disease',disease,'')
    ret+=basic_row.format('Protocol',protocol,'bg-light')
    ret+=basic_row.format('Methodology',method,'')
    ret+=basic_row.format('Accession',acc,'bg-light')
    ret+=basic_row.format('Gender',gender,'')
    ret+=basic_row.format('Age',age,'bg-light')
    ret+=basic_row.format('Stage',stage,'')
    ret+=basic_row.format('Sample list',sample_acc,'bg-light')
    ret+=basic_row.format('Citation',citation,'')

    print(ret)
except Exception as e:
      print('An error occurred when fetching information.')