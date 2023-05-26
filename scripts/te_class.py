###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-17 14:53:04
 # @modify date 2023-05-22 15:45:01
 # @desc [description]
###
import pandas as pd 
import sys

input_=sys.argv[1]
output_=sys.argv[2]
te_table=pd.read_csv(input_,sep='\t')
te_table['repFamily']=te_table['repFamily'].apply(lambda x: x.replace('?',''))

te_fam=open(output_,'w')
te_fam.write('''CREATE DATABASE IF NOT EXISTS scARE;
USE scARE;
DROP TABLE IF EXISTS TE_FAM;
CREATE TABLE TE_FAM (
    ID INT NOT NULL AUTO_INCREMENT,
    CLASS varchar(255) NOT NULL,
    FAMILY varchar(255) NOT NULL,
    Name varchar(255) NOT NULL,
    PRIMARY KEY (ID) 
);
''')
rte=te_table.loc[te_table['repClass'].isin(['LINE','SINE','LTR']),['repName','repClass','repFamily']].drop_duplicates()
for i in range(len(rte)):
    class_, family, name =rte.iloc[i,[1,2,0]]
    te_fam.write(f'INSERT INTO TE_FAM (CLASS,FAMILY,NAME) VALUES ("{class_}","{family}","{name}");\n')
te_fam.close()
