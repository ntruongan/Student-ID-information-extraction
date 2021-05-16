# -*- coding: utf-8 -*-
"""
Created on Sun May 16 14:01:24 2021

@author: ntruo
"""

#%%
import pytesseract
import shutil
import os
import cv2
import random
import re
import glob
try:
 from PIL import Image
except ImportError:
 import Image
import numpy as np
import matplotlib.pyplot as plt

#%%
DICT_RECTA = {0: 'id', 1: 'name', 2: 'dob', 3: 'major', 4: 'year_entry', 5: 'bank'}

rec = []
# id
lines = []
pointA = [25,435]
pointB = [25,490]
pointC = [260,435]
pointD = [260,490]
lines.append(pointA)    
lines.append(pointB)
lines.append(pointC)
lines.append(pointD)
rec.append(np.array(lines))


#name
rec = []
lines = []
pointA = [335,197]
pointB = [335,150]
pointC = [790,197]
pointD = [790,150]
lines.append(pointA)
lines.append(pointB)
lines.append(pointC)
lines.append(pointD)
rec.append(np.array(lines))
# rec = [np.array(rec)]

# birth
lines = []
pointA = [370,200]
pointB = [370,240]
pointC = [790,200]
pointD = [790,240]
lines.append(pointA)
lines.append(pointB)
lines.append(pointC)
lines.append(pointD)
rec.append(np.array(lines))


# major
lines = []
pointA = [370,240]
pointB = [370,280]
pointC = [790,240]
pointD = [790,280]
lines.append(pointA)
lines.append(pointB)
lines.append(pointC)
lines.append(pointD)
rec.append(np.array(lines))


#  year entry
lines = []
pointA = [400,310]
pointB = [400,350]
pointC = [790,310]
pointD = [790,350]
lines.append(pointA)
lines.append(pointB)
lines.append(pointC)
lines.append(pointD)
rec.append(np.array(lines))


# bank
lines = []
pointA = [250,353]
pointB = [250,385]
pointC = [790,353]
pointD = [790,385]
lines.append(pointA)
lines.append(pointB)
lines.append(pointC)
lines.append(pointD)
rec.append(np.array(lines))


#%%
# preprocessing
# gray scale
def gray(img):
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(r"./preprocess/img_gray.png",img)
    return img

# blur
def blur(img) :
    img_blur = cv2.GaussianBlur(img,(5,5),0)
    cv2.imwrite(r"./preprocess/img_blur.png",img)    
    return img_blur

# threshold
def threshold(img):
    #pixels with value below 100 are turned black (0) and those with higher value are turned white (255)
    img = cv2.threshold(img, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]    
    cv2.imwrite(r"./preprocess/img_threshold.png",img)
    return img
#%%

def img_preprocessing(path):
    img_or = cv2.imread(path)
    img_or = cv2.resize(img_or, (800,500))
    img = cv2.cvtColor(img_or, cv2.COLOR_BGR2GRAY)
    ksize = (5, 5)
    img = cv2.blur(img, ksize) 
    # img = cv2.blur(img, ksize) 
    img_th = cv2.threshold(img, 100, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C | cv2.THRESH_BINARY)[1] 
    kernel = np.ones((3,18),np.uint8)
    img = cv2.dilate(img_th, kernel, iterations = 1)
    return img, img_or
#%%
def name_generator(path, idx):
    assert '\\' in path
    assert path.endswith('_0.jpg') or path.endswith('_0.JPG')
    names = path.split('\\')
    name = '%s%s%s.%s' % (names[-2], names[-1].split('.')[0], str(idx),names[-1].split('.')[1])
    return name

def save_image(folder, name, img):
    assert name.endswith('.jpg') or name.endswith('.JPG')
    path = '%s/%s' % (folder, name)
    if cv2.imwrite(path, img):
        return True
    else:
        return False


#%%
def get_contours(paths, contours = None):
    dict_map = {}
    config = ('-l vie --oem 1 --psm 3')
    for path in paths:
        img, img_or = img_preprocessing(path)
        if contours == None:
            contours, hierarchy = cv2.findContours(img, 
                                                    cv2.RETR_EXTERNAL, 
                                                    cv2.CHAIN_APPROX_NONE)
            for idx, cnt in enumerate(contours): 
                if cv2.contourArea(cnt)>800 and cv2.contourArea(cnt)<10000:
                    x, y, w, h = cv2.boundingRect(cnt) 
                    if x >= 3 and y >=3 and y + h + 3 <= 500 and x + w + 3 <=800:
                        # rect = cv2.rectangle(img_or, (x, y), (x + w, y + h), (0, 255, 255),2)
                        cv2.imshow('cnt', img_or)
                        cropped = img_or[y-3:y + h+3, x-3:x + w+3] 
                        #cv2.imshow('cnst%d'%idx,cropped)
                        text = pytesseract.image_to_string(cropped, config=config) 
                        print(text)
                        # if text != None:
                        # text_re = re.sub(r"[\n,'-;]","",text).strip()
                        if text != '':
                            print(text)
                            name = name_generator(path, idx)
                            save_image('id_part', name, cropped)
                            dict_map[name] = text
                        else: 
                            print(text)
        else:
            for idx, cnt in enumerate(contours): 
                x, y, w, h = cv2.boundingRect(cnt) 
                cropped = img_or[y:y + h, x:x + w] 
                text = pytesseract.image_to_string(cropped, config=config) 
                name = name_generator(path, DICT_RECTA[idx])
                # print(text)
                text_re = re.sub(r"[\n]","",text).strip()
                if text_re != '':
                    # print(text)
                    
                    save_image('id_part', name, cropped)
                    dict_map[name] = text_re

            
        
                        
    return dict_map

#%%

def to_csv(dict_map):
    with open('mapping_id.csv', 'w', encoding='utf-8') as f:
        for key in dict_map.keys():
            f.write("%s,%s\n"%(key,dict_map[key]))
#%%



if __name__ == '__main__':
    mapping = {}
    paths = glob.glob('data/*/*_0.jpg')
    # path = r'D:\IT\Nam_3\HK2\DL\Final_Project\data\CHS\17110301_0.jpg'
    # idx = np.random.randint(0, len(paths))
    # print(idx)
    # paths = [r'D:\IT\Nam_3\HK2\DL\Final_Project\data\GTQ\18143347_0.jpg']
    mapping = get_contours(paths,rec)
    to_csv(mapping)

