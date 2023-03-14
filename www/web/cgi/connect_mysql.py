#!/usr/bin/python3
import cgitb

cgitb.enable()
print( 'Content_Type:text/html\n\n')
import subprocess

print(subprocess.check_output('touch /var/run/mysqld/mysqld.sock 2>&1',shell=True))

import os
import MySQLdb # import the MySQLdb module

# Create the connection object
connection = MySQLdb.connect(
    user='www-data',
    passwd='www-data-passwd',
    host='localhost',
    port=13306,
    db='scARE'
)

# Create cursor and use it to execute SQL command
cursor = connection.cursor()
cursor.execute("select * from TE_FAM")

info=cursor.fetchone()
while info :
    print(info)
    info=cursor.fetchone()
