# -*- coding: utf-8 -*-
"""
Created on Tue May 18 16:01:43 2021

@author: ntruo
"""

alphabets = u"AÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬBCDĐEẺẼẸÉÈÊẾỀỂỄỆFGHIÍÌỈĨỊJKLMNOÓÒỎÕỌÔỐỒỔỖỘƠỢỞỠỜỚPQRSTUÚÙỦŨỤƯỨỪỬỮỰVWXYÝỴỲỶỸZ"
lower = alphabets.lower()
spe = u"0123456789/-.:& " 
alphabets = alphabets+lower+spe
# alphabets

import json 
import glob
def string_exis(s1,s2):
    for s in s2:
        if s1==s:
            return True
    return False
f = open(r'D:\IT\Nam_3\HK2\DL\Final_Project\vietnamese_ocr-master\mapping.json',encoding = 'utf-8')
dict_ = json.load(f)
paths = glob.glob('img\*')
paths = [path.split('\\')[1] for path in paths]
for path in paths:
    # print(val)
    # for path in paths:
    if string_exis(path,dict_.keys()):
        continue
    else:
        print(path)
        
for path in dict_.keys():
    # print(val)
    # for path in paths:
    if string_exis(path,paths):
        continue
    else:
        print(path)
                
    
    
    