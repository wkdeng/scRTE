###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-06-14 17:15:57
 # @modify date 2023-06-14 17:42:07
 # @desc [description]
###
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon
import os

datasets=[x.split('.')[0] for x in os.listdir('../data/all_datasets') if x.endswith('.cell_exp.txt')]
print(datasets)
