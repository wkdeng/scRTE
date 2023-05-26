#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-16 15:30:14
 # @modify date 2023-05-16 15:30:14
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
class_=form['Class'].value
family=form['Family'].value
name=form['Name'].value

# Create the connection object
connection = MySQLdb.connect(
    user='www-data',
    passwd='www-data-passwd',
    host='127.0.0.1',
    port=3306,
    db='scARE'
)

cursor = connection.cursor()
sql="select CLASS,FAMILY,NAME,GENE from TE_GENE where CLASS='%s' and FAMILY='%s' and NAME='%s'"%(class_,family,name)
cursor.execute(sql)
info=cursor.fetchall()

table_content = '''<table class="table table-striped" id='gene_table'><thead><tr><th scope="col">Class</th><th scope="col">Family</th><th scope="col">Name</th><th scope="col">Gene</th></tr></thead><tbody>{table_row}</tbody></table>'''

table_row = ''
row_fmt = '''<tr><td>{Class}</td><td>{Family}</td><td>{Name}</td><td><a href='{link}' target='_blank'>{Gene}</a></td></tr>'''
if info:
    for row in info:
        Class,Family,Name,Gene=row
        link=f'https://www.genecards.org/cgi-bin/carddisp.pl?gene={Gene}' if not Gene.startswith('ENSG') else f"https://useast.ensembl.org/Homo_sapiens/Gene/Summary?g={Gene}"
        table_row += row_fmt.format(Class=Class, Family=Family, Name=Name,Gene=Gene,link=link)


if len(table_row) == 0:
    print('No gene contains this RTE in database.')
else:
    print(table_content.format(table_row=table_row))