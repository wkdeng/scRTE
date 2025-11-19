#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-17 15:54:50
 # @modify date 2023-03-17 15:54:50
 # @desc [description]
#############################
import cgitb
import subprocess
import os
# import MySQLdb
import pandas as pd

cgitb.enable()
print( 'Content_Type:text/html; charset=utf-8\r\n\n')

table_content='''
<table >
  <thead>
    <tr>
    <th class='class'>Class
    </th>
    <th>
        <table>
            <thead>
                <th class='inner'>Family</th>
                <th class='inner'>Name</th>
            </thead>
        </table>
    </th>
    </tr>
  </thead>
  <tbody>
  {class_row}
  </tbody>
  </table>
'''

class_content='''
    <tr class="collapsible">
        <td class='class'>{Class}</td>
        <td class="family_0">
            <table>
                {family_row}
            </table>
        </td>
    </tr>
'''

family_content='''
      <tr class="family_0" name='parent of {Family}'>
      <td class="family">{Family}</td>
      <td class='name'>
        <ul class="content">
        {name_row}
        </ul>
      </td>
      </tr>
'''
name_content="""<li class='{name_cls}' style="list-style-type:none;display:{display}"><a href="http://localhost/te_info.html?Class={Class}&Family={Family}&Name={name_name}" target="_blank">{name_name}</li>"""


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
    # Create cursor and use it to execute SQL command
    cursor.execute("select * from TE_FAM")
    info=cursor.fetchall()
    info=pd.DataFrame(info)
    info.columns=['ID','Class','Family','Name']
    info.sort_values(by=['Class','Family','Name'],inplace=True)


    table_full=""
    class_row=""
    family_row=""
    name_row=""
    current_family=""
    current_class=""
    first_fam=True
    first_class=True
    first_name=True

    for i in range(len(info)):

        Class,Family,Name=info.iloc[i,[1,2,3]]


        if Family==current_family:
            first_fam=False
        else:
            first_fam=True
            first_name=True

        if Class==current_class:
            first_class=False
        else:
            first_class=True
            first_fam=True
            first_name=True


        if len(name_row)>0:
            if first_fam:
                family_row+=family_content.format(name_row=name_row,Family=current_family)
                name_row=""

        if len(family_row)>0:
            if first_class:
                class_row+=class_content.format(family_row=family_row,Class=current_class)
                family_row=""

        # if first_class:
        #     table_full+=class_row
        #     class_row=""

        current_family=Family
        current_class=Class

        name_cls='c1' if first_name else 'c2'
        display='block' if first_name else 'none'
        first_name=False
        name_row+=name_content.format(name_cls=name_cls,name_name=Name,display=display,Family=current_family,Class=current_class)

    family_row+=family_content.format(name_row=name_row,Family=current_family)
    class_row+=class_content.format(family_row=family_row,Class=current_class)
    table_full+=class_row

    print(table_content.format(class_row=table_full))
except Exception as e:
      print('An error occurred when fetching information.')