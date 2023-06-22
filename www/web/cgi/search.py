#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
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
# import MySQLdb
import pandas as pd
import cgi
import config

cgitb.enable()
print('Content_Type:text/html; charset=utf-8\r\n\n')

try:
    form = cgi.FieldStorage()
    field = form['field'].value
    
    if 'kw' not in form or len(form['kw'].value) == 0:
        print('Please input keywords.')
        exit()
    kw = form['kw'].value
    type_ = form['type'].value
    bool_rel = 'Any'
    lucky=form['lucky'].value

    if 'bool_rel' in form:
        bool_rel = form['bool_rel'].value

    bool_rel2 = 'AND' if bool_rel == 'All' else 'OR'

    kw_org = kw
    kw = kw.replace("'", "\\'")
    if type_ == 'multi':
        kw = kw.strip().split('\n')
        kw_org = kw_org.strip().split('\n')
    else:
        kw = [kw.strip()]
        kw_org = [kw_org.strip()]

    cursor,cnx=config.get_cursor()
    table_content = '''<table class="table table-striped" id='result_table'>  <caption>{caption}</caption><thead><tr><th scope="col">Class</th><th scope="col">Family</th><th scope="col">Name</th></tr></thead><tbody>{table_row}</tbody></table>'''
    disease_table_content = '''<table class="table table-striped" id='result_table'>  <caption>{caption}</caption><thead><th scope="col">Dataset</th><th scope="col">Disease</th><th scope="col">Cell type</th><th scope="col">Accession</th><tbody>{table_row}</tbody></table>'''
    gene_table_content = '''<table class="table table-striped" id='result_table'>  <caption>{caption}</caption><thead><tr><th scope="col">Class</th><th scope="col">Family</th><th scope="col">Name</th><th scope="col">Gene</th></tr></thead><tbody>{table_row}</tbody></table>'''
    if field == 'RTE':
        table_row = ''
        row_fmt = '''<tr><td>{Class}</td><td>{Family}</td><td><a href='te_info.html?Class={Class}&Family={Family}&Name={Name}' target='_blank'>{Name}</td></tr>'''

        conditioni = " (NAME LIKE '%{kwi}%' OR FAMILY LIKE '%{kwi}%' OR CLASS LIKE '%{kwi}%') "
        condition = bool_rel2.join([conditioni.format(kwi=kwi) for kwi in kw])
        sql = f"select * from TE_FAM WHERE {condition}"
        cursor.execute(f"select * from TE_FAM WHERE {condition}")
        info = cursor.fetchall()
        if info:
            for row in info:
                Class = row[1]
                Family = row[2]
                Name = row[3]
                table_row += row_fmt.format(Class=Class, Family=Family, Name=Name)
                if lucky == 'true':
                    break
        if len(table_row) == 0:
            print('No such RTE in database')
        else:
            caption = 'Search result in field <strong>{field}</strong> matches <strong>{bool_rel}</strong> of <strong>"{kwi}"</strong> '.format(
                kwi=';'.join(kw_org), field=field, bool_rel=bool_rel)
            print(table_content.format(table_row=table_row, caption=caption))

    elif field == 'Gene':
        table_row = ''
        row_fmt = '''<tr><td>{Class}</td><td>{Family}</td><td><a href='te_info.html?Class={Class}&Family={Family}&Name={Name}' target='_blank'>{Name}</td><td>{Gene}</td></tr>'''

        conditioni = " (GENE LIKE '%{kwi}%') "
        condition = bool_rel2.join([conditioni.format(kwi=kwi) for kwi in kw])
        cursor.execute(f"select * from TE_GENE WHERE  {condition}")
        info = cursor.fetchall()
        if info:
            for row in info:
                Class = row[1]
                Family = row[2]
                Name = row[3]
                Gene = row[4]
                table_row += row_fmt.format(Class=Class,
                                            Family=Family, Name=Name, Gene=Gene)
                if lucky == 'true':
                    break
        if len(table_row) == 0:
            print('No such RTE in database')
        else:
            caption = 'Search result in field <strong>{field}</strong> matches <strong>{bool_rel}</strong> of <strong>"{kwi}"</strong> '.format(
                kwi=';'.join(kw_org), field=field, bool_rel=bool_rel)
            print(gene_table_content.format(table_row=table_row, caption=caption))

    elif field == 'Disease':
        table_row = ''
        row_fmt = '''<tr><td><a href='dataset_detail.html?KW={Dataset}&Cate=Dataset' target='_blank'>{Dataset}</td><td>{Disease}</td><td>{CellType}</td><td><a href='{accession_link}' target='_blank'>{Accession}</a></td></tr>'''

        conditioni = " (DISEASE LIKE '%{kwi}%') "
        condition = bool_rel2.join([conditioni.format(kwi=kwi) for kwi in kw])
        cursor.execute(f"select * from DATASET_META WHERE  {condition}")
        info = cursor.fetchall()
        if info:
            for row in info:
                Disease = row[4]
                Dataset = row[0]
                CellType = ', '.join(row[7].split(';'))
                Accession = row[8]
                if Accession.startswith('GSE'):
                    accession_link = f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={Accession}'  
                elif Accession.startswith('syn'):
                    accession_link=f'https://synapse.org/#!Synapse:{Accession}'
                else:
                    accession_link = f'https://www.ncbi.nlm.nih.gov/bioproject/{Accession}'
                table_row += row_fmt.format(Dataset=Dataset, Disease=Disease,
                                            CellType=CellType, Accession=Accession, accession_link=accession_link)
                if lucky == 'true':
                    break
        if len(table_row) == 0:
            print('No such disease in database')
        else:
            caption = 'Search result in field <strong>{field}</strong> matches <strong>{bool_rel}</strong> of <strong>"{kwi}"</strong> '.format(
                kwi=';'.join(kw_org), field=field, bool_rel=bool_rel)
            print(disease_table_content.format(
                table_row=table_row, caption=caption))

    elif field == 'Dataset':
        table_row = ''

        conditioni = " (scARE_ID LIKE '%{kwi}%') "
        condition = bool_rel2.join([conditioni.format(kwi=kwi) for kwi in kw])
        cursor.execute(f"select * from DATASET_META WHERE  {condition}")
        info = cursor.fetchall()
        if info:
            for row in info:
                Disease = row[4]
                Dataset = row[0]
                CellType = ', '.join(row[7].split(';'))
                Accession = row[8]
                accession_link = f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={Accession}' if Accession.startswith(
                    'GSE') else f'https://synapse.org/#!Synapse:{Accession}'
                table_row += f'''<tr><td><a href='dataset_detail.html?KW={Dataset}&Cate=Dataset' target='_blank'>{Dataset}</td><td>{Disease}</td><td>{CellType}</td><td><a href='{accession_link}' target='_blank'>{Accession}</a></td></tr>'''
                if lucky == 'true':
                    break
        if len(table_row) == 0:
            print('No such dataset in database')
        else:
            caption = 'Search result in field <strong>{field}</strong> matches <strong>{bool_rel}</strong> of <strong>"{kwi}"</strong> '.format(
                kwi=';'.join(kw_org), field=field, bool_rel=bool_rel)
            print(disease_table_content.format(
                table_row=table_row, caption=caption))
    else:
        print('Implement later')
except Exception as e:
    print('An error occurred when fetching information.')