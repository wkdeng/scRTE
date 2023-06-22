#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
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
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')
import config

form=cgi.FieldStorage()
cell=form['Cell'].value

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
  if cell not in ['All','Ex','In','Mic','Ast','OPC','Oli','VLMC']:
    raise Exception('Cell type not found.')
  sql=f"select scARE_ID from DATASET_META where CELL_TYPE like '%{cell}%'; "
  cursor,cnx=config.get_cursor()
  cursor.execute(sql)
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
          <button class="btn" data-toggle="collapse" data-target="#{dataset}_ct" aria-expanded="{expand}" aria-controls="{dataset}_ct" onclick="load_data(this);">
            {dataset}
          </button>
          <a href="dataset_detail.html?Cate=Dataset&KW={dataset}&CL=F" target="_blank">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-up-right" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/>
            <path fill-rule="evenodd" d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/>
          </svg>
          </a>
        </h5>
      </div>

      <div id="{dataset}_ct" class="collapse {show}" aria-labelledby="{dataset}_head" data-parent="#{dataset}">
        <div class="card-body border-0 dataset_hide" style="min-height: 900px">{dataset_info}</div>
      </div>
  </div>
    '''
  expand='true'
  show='show'
  card_bodys=''
  src='src'
  for dataset in info:
      dataset=dataset[0]
      dataset_info=f'<iframe class="border-0" width="100%" height="850px" {src}="dataset_detail.html?Cate=Dataset&KW={dataset}&CL=T"></iframe>'
      card_bodys+=card_body.format(dataset=dataset,dataset_info=dataset_info,expand=expand,show=show)
      src='data-src'
      expand='false'
      show=''

  card=card.format(dataset=cell,card_bodys=card_bodys)
  print(card)
except Exception as e:
      print('An error occurred when fetching information.')