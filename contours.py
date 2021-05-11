# -*- coding: utf-8 -*-
"""
Created on Sun May  9 17:23:28 2021

@author: ntruo
"""

import pytesseract
import cv2
import re
import numpy as np
import glob



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



def get_contours(path):
    
    img, img_or = img_preprocessing(path)
    contours, hierarchy = cv2.findContours(img, 
                                            cv2.RETR_EXTERNAL, 
                                            cv2.CHAIN_APPROX_NONE)

    for idx, cnt in enumerate(contours): 
        if cv2.contourArea(cnt)>1000 and cv2.contourArea(cnt)<10000:
            x, y, w, h = cv2.boundingRect(cnt) 
            if x >= 10 and y >=5 and y + h + 5 <= 500 and x + w + 10 <=800:
                # rect = cv2.rectangle(img_or, (x, y), (x + w, y + h), (0, 255, 255),2)
                # cv2.imshow('cnt',img)
                cropped = img_or[y-5:y + h+5, x-10:x + w+10] 
                # cv2.imshow('cnst%d'%idx,cropped)
                config = ('-l vie --oem 1 --psm 3')
                
                text = pytesseract.image_to_string(cropped, config=config) 
                # if text != None:
                text = re.sub(r"[\n\x0c,'-;]","",text).strip()
                if text != '':
                    name = name_generator(path, idx)
                    save_image('text_image', name, cropped)
                    print(text)
                    print(name)

def name_generator(path, idx):
    assert '\\' in path
    assert path.endswith('_0.jpg')
    names = path.split('\\')
    name = '%s%s%s.%s' % (names[-2], names[-1].split('.')[0], str(idx),names[-1].split('.')[1])
    return name

def save_image(folder, name, img):
    assert name.endswith('.jpg')
    path = '%s/%s' % (folder, name)
    if cv2.imwrite(path, img):
        return True
    else:
        return False

def mapping(paths):
    for path in paths:
         

if __name__ == '__main__':
    mapping = {}
    paths = glob.glob('data/*/*_0.jpg')
    # path = r'D:\IT\Nam_3\HK2\DL\Final_Project\data\CHS\17110301_0.jpg'
    idx = np.random.randint(0, len(paths))
    print(idx)
    get_contours(paths[idx])

    