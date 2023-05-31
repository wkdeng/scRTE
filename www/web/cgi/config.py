import json
import os

current_folder=os.path.abspath('.')
if current_folder.endswith('te_info'):
    config_path='../config.json'
else:
    config_path='config.json'
host,user,passwd,port,db=json.load(fp=open(config_path,'r'))
