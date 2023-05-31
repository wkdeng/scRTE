#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-01 14:37:55
 # @modify date 2023-05-01 14:37:55
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

form=cgi.FieldStorage()
cell=form['Cell'].value
cursor = connection.cursor()

cursor.execute(f"select scARE_ID from DATASET_META where CELL_TYPE like '%{cell}%'; ")

info=cursor.fetchall()



card='''
<h5 class="card-header"><strong>Datasets contains {dataset}</strong></h5>
<div class="card-body">
  {card_bodys}
</div>
'''
card_body='''
<div class="card mb-0" id="{dataset}"  >
    <div class="card-header" id="{dataset}_head">
      <h5 class="mb-0">
        <button class="btn" data-toggle="collapse" data-target="#{dataset}_ct" aria-expanded="{expand}" aria-controls="{dataset}_ct">
          {dataset}
        </button>
      </h5>
    </div>

    <div id="{dataset}_ct" class="collapse {show}" aria-labelledby="{dataset}_head" data-parent="#{dataset}">
      <div class="card-body border-0" style="min-height: 900px">
        {dataset_info}
    </div>
  </div>
  '''
expand='true'
show='show'
card_bodys=''
for dataset in info:
    dataset=dataset[0]
    dataset_info=f'<iframe class="border-0" width="100%" height="850px" src="dataset_detail.html?Cate=Dataset&KW={dataset}&CL=T"></iframe>'
    card_bodys+=card_body.format(dataset=dataset,dataset_info=dataset_info,expand=expand,show=show)
    expand='false'
    show=''


card_bodys+=card_body.format(dataset='AD_HS_00002',dataset_info=dataset_info,expand=expand,show=show)
card=card.format(dataset=cell,card_bodys=card_bodys)
print(card)