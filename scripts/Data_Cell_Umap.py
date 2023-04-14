###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-10 14:41:40
 # @modify date 2023-04-10 14:41:40
 # @desc [description]
###

import sys
import pandas as pd

cell_umap<-pd.read_csv(sys.argv[1],sep='\t',index_col=0)
