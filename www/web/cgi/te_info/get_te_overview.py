#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-04 17:24:37
 # @modify date 2023-05-04 17:24:37
 # @desc [description]
#############################

import cgitb
import pandas as pd
import cgi
import json
import MySQLdb
import urllib.parse
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



form = cgi.FieldStorage()
cls_=form['Class'].value
fam=form['Family'].value
name=form['Name'].value
# Create cursor and use it to execute SQL command
cursor = connection.cursor()

cursor.execute(f"select * from TE_BASIC WHERE CLASS = '{cls_}' AND FAMILY = '{fam}' AND NAME = '{name}'")
info=cursor.fetchone()

num_locus=info[6]
cons_len=info[5]
cons=info[4]


## basic row
basic_row='''
<div class="row mb-3">
<span class="col-md-4 {2}"><strong>{0}:</strong></span>
<span class="col-md-8 {2}" style="word-wrap: break-word;">{1}</span>
</div>
'''
basic=""
basic+=basic_row.format('Class',cls_,'bg-light')
basic+=basic_row.format('Family',fam,'')
basic+=basic_row.format('Name',name,'bg-light')
basic+=basic_row.format('Locus #',num_locus,'')
basic+=basic_row.format('Consensus Length',cons_len,'bg-light')
basic+=basic_row.format('Consensus',cons,'bg-light')

chr_dist=list(json.loads(info[7]))
chrdist_ret=[]
chrs=['chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM','others']
for i in range(26):
    chrdist_ret.append([chrs[i],chr_dist[i]])

dist_arr=json.loads(info[8])
dist_arr_ret=[]

for i in range(len(dist_arr)):
    for j in range(len(dist_arr[i])):
        dist_arr_ret.append([i,j,dist_arr[i][j]])

dist_genic=json.loads(info[9])
print(json.dumps([basic,chrdist_ret,dist_arr_ret,[['Genic',dist_genic[0]],['Intergenic',dist_genic[1]]]]))