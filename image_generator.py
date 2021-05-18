# -*- coding: utf-8 -*-
"""
Created on Sun May 16 19:18:30 2021

@author: ntruo
"""
import numpy as np
import cv2

def preprocess(img, max_shape):
    (h, w) = img.shape
    (shape_0, shape_1, _) = max_shape
    final_img = np.ones([shape_0, shape_1])*255 # blank white image
    
    # crop
    if w > shape_1:
        img = img[:, :shape_1]
        
    if h > shape_0:
        img = img[:shape_0, :]
    
    
    final_img[:h, :w] = img
    # return cv2.rotate(final_img, cv2.ROTATE_90_CLOCKWISE)
    return final_img
    


def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1])
  return result

#%%
image = cv2.imread(r'D:\IT\Nam_3\HK2\DL\Final_Project\text_image\CHS18104004_0name.jpg')
img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
img = rotate_image(img,-1)

# img = preprocess(img,(64,512,3))
cv2.imshow('z',img)
#%%

import pandas as pd

df.to_json (r'mapping.json')

#%%

import json  
       
# Data to be written  
dictionary ={  
  "id": "04",  
  "name": "sunil",  
  "depatment": "HR"
}  


#%%
import glob
import pandas as pd

df = pd.read_csv('mapping.csv',encoding = 'utf-8')
csv_paths = df["FILE_NAMES"][::].values
paths = glob.glob(r'D:\IT\Nam_3\HK2\DL\Final_Project\vietnamese_ocr-master\img\*')


len(csv_paths)
len(paths)



#%%
import json
# df = pd.read_csv (r'D:\IT\Nam_3\HK2\DL\Final_Project\mapping.csv')
dict_from_csv = pd.read_csv(r'D:\IT\Nam_3\HK2\DL\Final_Project\mapping.csv',encoding='utf-8', header=None, index_col=0, squeeze=True).to_dict()
# Serializing json   
json_object = json.dumps(dict_from_csv, ensure_ascii=False,indent=4)
print(json_object) 

with open('mapping2.json', 'w',encoding='utf-8') as fp:
    json.dump(dict_from_csv, fp, ensure_ascii=False,separators=(',\n', ':'))