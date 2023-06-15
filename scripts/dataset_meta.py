###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-17 14:53:04
 # @modify date 2023-05-31 15:14:48
 # @desc [description]
###
import pandas as pd 
import sys

# sys.argv=['','../data/Dataset.meta.txt','../www/mysql/meta.sql']
input_=sys.argv[1]
output_1=open(sys.argv[2],'w')

output_1.write('''use scARE;
    DROP TABLE IF EXISTS `DATASET_META`;
    CREATE TABLE `DATASET_META` (
    scARE_ID varchar(11) NOT NULL,
    STUDY varchar(255) NOT NULL,
    SAMPLE_NUMBER int(11) NOT NULL,
    SPECIES varchar(255) NOT NULL,
    DISEASE TEXT NOT NULL,
    BRAIN_REGION TEXT NOT NULL,
    DISEASE_STAGE TEXT NOT NULL,
    CELL_TYPE TEXT NOT NULL,
    ACCESSION TEXT NOT NULL,
    METHODOLOGY varchar(255) NOT NULL,
    PROTOCOL varchar(255) NOT NULL,
    GENDER TEXT NOT NULL,
    AGE TEXT NOT NULL,
    SAMPLE_ACCESSION TEXT NOT NULL,
    CITATION TEXT NOT NULL,
    PRIMARY KEY (scARE_ID));\n''')

output_2=open(sys.argv[3],'w')
output_2.write('''use scARE;
    DROP TABLE IF EXISTS `SAMPLE2DATASET`;
    CREATE TABLE `SAMPLE2DATASET` (
    scARE_ID varchar(11) NOT NULL,
    SAMPLE_ID varchar(255) NOT NULL,
    PRIMARY KEY (SAMPLE_ID));\n''')
meta_table=pd.read_csv(input_,sep='\t')
for i in range(meta_table.shape[0]):
    info=list(meta_table.iloc[i,:])
    output_1.write('INSERT INTO `DATASET_META` VALUES ('+','.join(['"'+str(x).replace("'","\\'").replace('"','\\"').replace("’","\\'")+'"' for x in info])+');\n');
    for sample in info[13].split(';'):
        output_2.write('INSERT INTO `SAMPLE2DATASET` VALUES ("'+info[0]+'","'+sample+'");\n')

output_1.close()
output_2.close()