#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 01:40:30 2020

@author: shariba
"""

import cv2
import numpy as np
import skimage.draw

#['Instrument', 'Specularity', 'Artefact' , 'Bubbles', 'Saturation', 'blood']
#classListBBOX=['Specularity', 'Saturation', 'Artefact', 'Blur', 'Contrast', 'Bubbles', 'Instrument', 'blood']

categoryList = ['BE', 'suspicious', 'HGD' , 'cancer', 'polyp', 'ulcer']

class_rgb = [
    (0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0),
    (128, 128, 0), (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128)]

def draw_line(img, x, y, height, width, color):
    cv2.line(img, (x, 0), (x, height), color, thickness=2)
    cv2.line(img, (0, y), (width, y), color, thickness=2)
    return img
# writing bbox
def save_bb(txt_path, line):
    with open(txt_path, 'a') as myfile:
        myfile.write(line + "\n") # append line
        
def voc_format(class_index, coord):
    # Order: xmin ymin xmax ymax class
    # Top left pixel is (1, 1) in VOC
    xmin = np.min(coord[:,0,0])+1
    ymin = np.min(coord[:,0,1])+1
    xmax = np.max(coord[:,0,0])+1
    ymax = np.max(coord[:,0,1])+1
    items = map(str, [xmin, ymin, xmax, ymax, class_index])
    return ' '.join(items)

def valRect(coord):
    xmin = np.min(coord[:,0,0])+1
    ymin = np.min(coord[:,0,1])+1
    xmax = np.max(coord[:,0,0])+1
    ymax = np.max(coord[:,0,1])+1
    return [xmin, ymin, xmax, ymax]

def getBBoxCordinatesFromMask_voc(image, im_mask, txt_path, classCategory, ll, debug=0):
    maskCordinates=cv2.findNonZero(im_mask)
    line = voc_format(classCategory, maskCordinates)
    save_bb(txt_path, line)
    [xmin, ymin, xmax, ymax] = valRect(maskCordinates)
    color = class_rgb[ll]
    img=cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
    return img

# write to the yolo format
def yolo_format(class_index, coord, width, height):
    [xmin, ymin, xmax, ymax] = valRect(coord)
    x_center = (xmin + xmax) / float(2.0 * width)
    y_center = (ymin + ymax) / float(2.0 * height)
    x_width = float(abs(xmax - xmin)) / width
    y_height = float(abs(ymax - ymin)) / height
    return str(class_index) + " " + str(x_center) \
       + " " + str(y_center) + " " + str(x_width) + " " + str(y_height)

def getBBoxCordinatesFromMask_yolo(image, im_mask, txt_path, classCategory, ll, width, height): 
    maskCordinates=cv2.findNonZero(im_mask)
    line=yolo_format(ll, maskCordinates, width, height)
    save_bb(txt_path, line)
    [xmin, ymin, xmax, ymax] = valRect(maskCordinates)
    color = class_rgb[ll]
    img1, contours, hierarchy = cv2.findContours(im_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours !=[]:
        midVal = int(contours[0].shape[0]/2)
#        cv2.drawContours(image, contours, -1, color, 3)
        cv2.putText(image, classCategory, (contours[0][midVal][0][0],  contours[0][midVal][0][1]),  cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        image=cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
    return image
