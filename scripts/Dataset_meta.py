###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-17 14:53:04
 # @modify date 2023-03-17 14:53:04
 # @desc [description]
###
import pandas as pd 
import sys

input_=sys.argv[1]
output_=open(sys.argv[2],'w')

output_.write('''use scARE;
    DROP TABLE IF EXISTS `DATASET_META`;
    CREATE TABLE `DATASET_META` (
    scARE_ID int(11) NOT NULL,
    STUDY varchar(255) NOT NULL,
    SAMPLE_NUMBER int(11) NOT NULL,
    SPECIES varchar(255) NOT NULL,
    DISSASE varchar(255) NOT NULL,
    BRAIN_REGION varchar(255) NOT NULL,
    DISSASE_STAGE varchar(255) NOT NULL,
    CELL_TYPE varchar(255) NOT NULL,
    ACCESSION varchar(255) NOT NULL,
    METHODOLOGY varchar(255) NOT NULL,
    PROTOCOL varchar(255) NOT NULL,
    GENDER varchar(255) NOT NULL,
    AGE varchar(255) NOT NULL,
    SAMPLE_ACCESSION TEXT NOT NULL,
    PRIMARY KEY (scARE_ID)''')

meta_table=pd.read_csv(input_,sep='\t')
for i in range(meta_table.shape[0]):
    info=list(meta_table.iloc[i,:])
    output_.write('INSERT INTO `DATASET_META` VALUES ('+','.join(['"'+str(x)+'"' for x in info]));
output_.close()