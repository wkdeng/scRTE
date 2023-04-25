#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-21 09:42:45
 # @modify date 2023-04-21 09:42:45
 # @desc [description]
#############################

import cgitb
import subprocess
import os
import MySQLdb
import pandas as pd
import cgi

cgitb.enable()
print( 'Content_Type:text/html; charset=utf-8\r\n\n')

form = cgi.FieldStorage()
field=form['field'].value
kw=form['kw'].value

# Create the connection object
connection = MySQLdb.connect(
    host='127.0.0.1',
    user='www-data',
    passwd='www-data-passwd',
    port=3306,
    db='scARE'
)

# Create the cursor object
cursor = connection.cursor()

table_content='''<table >  <caption>{caption}</caption><thead><th>Class</th><th>Family</th><th>Name</th></thead><tbody>{table_row}</tbody></table>'''
disease_table_content='''<table >  <caption>{caption}</caption><thead><th>Disease</th><th>Dataset</th><th>Dataset</th></thead><tbody>{table_row}</tbody></table>'''
if field=='RTE':
    ## Search name
    cursor.execute(f"select * from TE_FAM WHERE NAME LIKE '%{kw}%' OR FAMILY LIKE '%{kw}%' OR CLASS LIKE '%{kw}%'")
    info=cursor.fetchall()

    table_row=''
    if info:
        caption='Search result for {kw} in field {field}'.format(kw=kw,field=field)
        for row in info:
            Class=row[1]
            Family=row[2]
            Name=row[3]
            table_row+=f'''<tr><td>{Class}</td><td>{Family}</td><td><a href='TE_info.html?Class={Class}&Family={Family}&Name={Name}' target='_blank'>{Name}</td></tr>'''
        print(table_content.format(table_row=table_row,caption=caption))
    else:
        print('No such TE in database')
elif field=='Gene':
    cursor.execute(f"select * from TE_GENE WHERE GENE LIKE '%{kw}%' OR FAMILY LIKE '%{kw}%' OR CLASS LIKE '%{kw}%'")
    info=cursor.fetchall()

    table_row=''
    if info:
        caption='RTEs in gene {kw}'.format(kw=kw)
        for row in info:
            Class=row[1]
            Family=row[2]
            Name=row[3]
            table_row+=f'''<tr><td>{Class}</td><td>{Family}</td><td><a href='TE_info.html?Class={Class}&Family={Family}&Name={Name}' target='_blank'>{Name}</td></tr>'''
        print(table_content.format(table_row=table_row,caption=caption))
    else:
        print('No such gene in database')
elif field=='Disease':
    cursor.execute(f"select * from DATASET_META WHERE DISEASE LIKE '%{kw}%'")
    info=cursor.fetchall()
    if info:
        caption='Dataset of disease {kw}'.format(kw=kw)
        table_row=''
        for row in info:
            Disease=row[1]
            Dataset=row[2]
            table_row+=f'''<tr><td>{Disease}</td><td>{Dataset}</td><td><a href='dataset.html?Dataset={Dataset}' target='_blank'>{Dataset}</td></tr>'''
        print(table_content.format(table_row=table_row,caption=caption))
    else:
        print('No such disease in database')
else:
    print('Implement later')