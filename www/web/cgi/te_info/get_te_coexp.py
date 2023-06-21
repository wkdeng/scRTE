#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-06-07 14:22:32
 # @modify date 2023-06-07 14:22:32
 # @desc [description]
#############################

import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb
import sys
sys.path.append('../')
import config
from json import JSONEncoder
import numpy
from scipy.stats import pearsonr,ranksums
from sklearn.linear_model import LinearRegression

cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')

form = cgi.FieldStorage()
feature1=form['RTE'].value
feature2=form['Gene'].value

dataset=form['Dataset'].value
cell=form['Cell'].value
condition=form['Condition'].value
if condition!='Control':
    condition=dataset.split('_')[0]

try:
    cursor,cnx=config.get_cursor()

    cursor.execute(f"select TABLE_ID from GENE_DICT WHERE GENE='{feature1}' ")
    table_id1=cursor.fetchone()[0]
    cursor.execute(f"select TABLE_ID from GENE_DICT WHERE GENE='{feature2}' ")
    table_id2=cursor.fetchone()[0]

    ## get umap
    sql=f'''
    SELECT scARE_ID,CELL,CELL_TYPE,DISEASE from  DATA_CELLUMAP WHERE DATA_CELLUMAP.scARE_ID='{dataset}'
    '''

    cursor.execute(sql)
    info=cursor.fetchall()
    cell_umap=pd.DataFrame(info)
    cell_umap.columns=['scARE_ID','CELL','CELL_TYPE','DISEASE']

    sql=f'''SELECT CELL,scARE_ID,{feature1} from CELL_EXP_{table_id1} WHERE CELL_EXP_{table_id1}.scARE_ID = "{dataset}"'''
    cursor.execute(sql)
    info=cursor.fetchall()
    exp1=pd.DataFrame(info)
    exp1.columns=['CELL','scARE_ID',feature1]


    sql=f'''SELECT CELL,scARE_ID,{feature2} from CELL_EXP_{table_id2} WHERE CELL_EXP_{table_id2}.scARE_ID = "{dataset}"'''
    cursor.execute(sql)
    info=cursor.fetchall()
    exp2=pd.DataFrame(info)
    exp2.columns=['CELL','scARE_ID',feature2]

    df=pd.merge(cell_umap,exp1,on=['CELL','scARE_ID'])
    df=pd.merge(df,exp2,on=['CELL','scARE_ID'])

    df=df.loc[df['DISEASE']==condition]
    df=df.loc[df['CELL_TYPE']==cell]

    
    class NumpyArrayEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, numpy.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)

    dots=json.dumps(df.loc[:,[feature1,feature2]].to_numpy(), cls=NumpyArrayEncoder)

    ## get boxplot
    boxplot=[{'name':'Most expressed TE','data':[]}]
    min_,q1,median,q3,max_=df[feature2].describe()[['min','25%','50%','75%','max']].values
    boxplot[0]['data'].append({'x':1,'low':min_,'q1':q1,'median':median,'q3':q3,'high':max_,'fillColor':'#f7a35c'})
    min_,q1,median,q3,max_=df[feature1].describe()[['min','25%','50%','75%','max']].values
    boxplot[0]['data'].append({'x':0,'low':min_,'q1':q1,'median':median,'q3':q3,'high':max_,'fillColor':'#7cb5ec'})
    labels=[feature1,feature2]

    ## get stats
    model = LinearRegression()
    model.fit(df[feature1].values.reshape(-1, 1), df[feature2].values.reshape(-1, 1))
    r_sq = model.score(df[feature1].values.reshape(-1, 1), df[feature2].values.reshape(-1, 1))
    intercept, slope = model.intercept_, model.coef_

    ranksums_=ranksums(df[feature1],df[feature2])
    pearsonr_=pearsonr(df[feature1],df[feature2])
    regression_line=json.dumps(["{:.2f}".format(r_sq),"{:.2e}".format(pearsonr_[1]),[min_,model.predict([[min_]])[0][0]],[max_,model.predict([[max_]])[0][0]]])

    print(json.dumps({'dots':dots,'regression_line':regression_line,'boxplot':boxplot,'labels':labels}))
except Exception as e:
    print(json.dumps(['No data','No data']))