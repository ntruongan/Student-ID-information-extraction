# -*- coding: utf-8 -*-
"""
Created on Mon May 17 23:11:09 2021

@author: ntruo
"""

import json
import pandas as pd
# df = pd.read_csv (r'D:\IT\Nam_3\HK2\DL\Final_Project\mapping.csv')
dict_from_csv = pd.read_csv(r'D:\IT\Nam_3\HK2\DL\Final_Project\data\Generator\mapping_id.csv',encoding='utf-8', header=None, index_col=0, squeeze=True).to_dict()
# Serializing json   
json_object = json.dumps(dict_from_csv, ensure_ascii=False,indent=4)
print(json_object) 

with open('mapping_mydrop.json', 'w+',encoding='utf-8') as fp:
    json.dump(dict_from_csv, fp, ensure_ascii=False,separators=(',\n', ':'))