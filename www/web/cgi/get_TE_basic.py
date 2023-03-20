#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-17 15:55:22
 # @modify date 2023-03-17 15:55:22
 # @desc [description]
#############################
import cgitb
import subprocess
import os
import MySQLdb
import pandas as pd
import cgi
import urllib.parse

cgitb.enable()
print( 'Content_Type:text/html; charset=utf-8\r\n\n')


# Create the connection object
connection = MySQLdb.connect(
    user='www-data',
    passwd='www-data-passwd',
    host='127.0.0.1',
    port=3306,
    db='scARE'
)
form = cgi.FieldStorage()
Class=form['Class'].value
Family=form['Family'].value
Name=form['Name'].value
# Create cursor and use it to execute SQL command
cursor = connection.cursor()

cursor.execute(f"select * from TE_BASIC WHERE CLASS = '{Class}' AND FAMILY = '{Family}' AND NAME = '{Name}'")
info=cursor.fetchone()

Num_locus=info[6]
Cons_len=info[5]
Cons=info[4]

chr_dist=urllib.parse.quote(info[7])
basic_row=f'''
<ul>
<li>{Class}</li>
<li>{Family}</li>
<li>{Name}</li>
<li>{Num_locus}</li>
<li>{Cons_len}</li>
<li>{Cons}</li>
</ul>
'''

chr_dist=f'''
<br/>
Distribution on Chromosomes<br/>
<iframe src="http://localhost:13838/Brain_scARE/chr_dist/?chr_dist={chr_dist}" style="border: 1px solid #AAA; width: 500px; height: 250px"></iframe>
'''

table_content=f'''
<table >
    <thead>
        Overview
    </thead>
    <tbody>
        <tr>{basic_row}</tr>
        <tr>{chr_dist}</tr>
        <tr></tr>
    </tbody>
</table>
'''
print(table_content)


        # 
        # <tr>{chr_ea_dist}</tr>
        # <tr>{gene_dist}</tr>