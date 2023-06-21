#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-29 17:00:59
 # @modify date 2023-03-29 17:00:59
 # @desc [description]
#############################
import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')


form = cgi.FieldStorage()
Class=form['Class'].value
Family=form['Family'].value
Name=form['Name'].value
Degree=form['Degree'].value

try:
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
    cursor.execute(f"select NAME, {Degree} from TE_NET WHERE CLASS = '{Class}' AND FAMILY = '{Family}' AND NAME = '{Name}'")
    info=cursor.fetchone()


    if info is None:
        print('{"nodes":[{"id":"%s","label":"%s","group":1}],"links":[{ "source":"%s","target":"%s","value":1}]}'%(Name,Name,Name,Name))
    else:
        print(info[1])
except Exception as e:
      print('An error occurred when fetching information.')