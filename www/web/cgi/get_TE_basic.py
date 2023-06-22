#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
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
# import MySQLdb
import pandas as pd
import cgi
import urllib.parse
import tempfile
import json

cgitb.enable()
print( 'Content_Type:text/html; charset=utf-8\r\n\n')


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
try:
    cursor,cnx=config.get_cursor()
    form = cgi.FieldStorage()
    Class=form['Class'].value
    Family=form['Family'].value
    Name=form['Name'].value
    # Create cursor and use it to execute SQL command

    cursor.execute(f"select * from TE_BASIC WHERE CLASS = '{Class}' AND FAMILY = '{Family}' AND NAME = '{Name}'")
    info=cursor.fetchone()

    Num_locus=info[6]
    Cons_len=info[5]
    Cons=info[4]

    chr_dist=urllib.parse.quote(info[7])


    ## basic row
    basic_row=f'''
    <ul>
    <li>Class: {Class}</li>
    <li>Family: {Family}</li>
    <li>Name: {Name}</li>
    <li>Number of locus: {Num_locus}</li>
    <li>Consensus sequence length: {Cons_len}</li>
    <li>Consensus sequence: {Cons}</li>
    </ul>
    '''

    ## distribution of locus number in chromosome
    chr_dist=f'''
    <br/>
    Distribution on Chromosomes<br/>
    <iframe src="http://localhost:3838/Brain_scARE/chr_dist/?chr_dist={chr_dist}" style="border: 1px solid #AAA; width: 500px; height: 250px"></iframe>
    '''

    ## distribution of locus in each chromosome
    chr_ea=info[8]

    tmp_file=next(tempfile._get_candidate_names())
    fp=open('/tmp/chr_ea_%s'%tmp_file,'w')
    fp.write(chr_ea)
    fp.close()

    _=subprocess.check_output(f"echo 'sleep 300 && rm /tmp/chr_ea_{tmp_file}'  ",shell=True).decode('utf-8')

    chr_ea=f'''
    <br/><br/>
    Distribution on each Chomosome<br/>
    <iframe src="http://localhost:3838/Brain_scARE/chr_ea/?tmp_file=chr_ea_{tmp_file}" style="border: 1px solid #AAA; width: 500px; height: 250px"></iframe>
    '''

    ## distribution of gene/intergenic region
    gene_inter=urllib.parse.quote(info[9])
    gene_inter=f'''
    <br/><br/>
    Distribution on genic/intergenic regions<br/>
    <iframe src="http://localhost:3838/Brain_scARE/gene_inter/?gene_inter={gene_inter}" style="border: 1px solid #AAA; width: 500px; height: 250px"></iframe>
    '''

    ## gene-te connection
    te_node=urllib.parse.quote(f'{Class}:{Family}:{Name}')
    gene_te_net=f'''
    <br/><br/>
    Gene-TE connection map<br/>
    <iframe src="http://localhost:3838/Brain_scARE/gene_te_net/?te_node={te_node}" style="border: 1px solid #AAA; width: 700px; height: 500px"></iframe>
    '''

    table_content=f'''
    <table >
        <thead>
            Overview
        </thead>
        <tbody>
            <tr>{basic_row}</tr>
            <tr>{chr_dist}</tr>
            <tr>{chr_ea}</tr>
            <tr>{gene_inter}</tr>
            <tr>{gene_te_net}</tr>
        </tbody>
    </table>
    '''
    print(table_content)
except Exception as e:
      print('An error occurred when fetching information.')