#!/usr/bin/python3
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-14 14:57:27
 # @modify date 2023-04-14 14:57:27
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
cell=form['Cell'].value


## cell number in each disease
