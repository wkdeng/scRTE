#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-05-15 10:29:45
 # @modify date 2023-05-15 10:29:45
 # @desc [description]
#############################

import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb
from collections import defaultdict
import math

cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

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
    sql="select NAME, CLASS, FAMILY, NUM_OCCUR from TE_BASIC"
    cursor.execute(sql)
    info=cursor.fetchall()


    treeview_result=[]
    class_order={}
    family_order=defaultdict(dict)

    for row in info:
        name, class_, family, num=row
        # num=math.log(num+1,10)


    

    # form=cgi.FieldStorage()
    # view=form.getvalue("view")
    ############ for static treemap ############

    treemap_ret=[]
    # if view=='treemap':
    info=pd.DataFrame(info, columns=["name", "class", "family", "value"]).sort_values(by=["class", "family", "name"])
    treemap_ret=[]
    class_imported=[]
    family_imported=[]


    table_head='''<table id="te_table" class="display stripe hover cell-border row-border order-column compact"><thead><tr><th>Class</th><th>Family</th><th>TE</th><th>Number of Occurrence</th></tr></thead><tbody>{table_row}</tbody></table>'''
    table_row=''
    table_row_fmt='''<tr><td>{class_}</td><td>{family}</td><td><a href='te_info.html?Name={name}&Class={class_}&Family={family}' target='_blank'>{name}</a></td><td>{num}</td></tr>'''


    for i in range(len(info)):
        name, class_, family, num=info.iloc[i]
        table_row+=table_row_fmt.format(class_=class_, family=family, name=name, num=num)

        if class_ not in class_order:
            class_order[class_]=len(class_order)
            family_order[class_]={}
            treeview_result.append({"name":class_, 'type':'cls',"children":[]})
        if family not in family_order[class_]:
            family_order[class_][family]=len(family_order[class_])
            treeview_result[class_order[class_]]["children"].append({"name":family,'type':'fam', "children":[]})
        treeview_result[class_order[class_]]["children"][family_order[class_][family]]["children"].append({"name":name, 'type':'subfam',"value":int(num),'link':f'te_info.html?Name={name}&Class={class_}&Family={family}'})

        if class_ not in class_imported:
            class_imported.append(class_)
            treemap_ret.append({'name':class_,'size':None})
        if family not in family_imported:
            family_imported.append(family)
            treemap_ret.append({'name':f'{class_}.{family}','size':None})
        treemap_ret.append({'name':f'{class_}.{family}.{name}','size':int(num)})

    print(json.dumps([table_head.format(table_row=table_row), treemap_ret,{'name':"TE", "children":treeview_result}]))
    # print(json.dumps(info.to_dict(orient='records')))
except Exception as e:
      print('An error occurred when fetching information.')