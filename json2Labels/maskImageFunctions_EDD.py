#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:08:29 2020

@author: shariba
"""

from skimage import io
import skimage.draw
import os
from tifffile import imsave
import numpy as np
import shutil

from extractBboxFromMask_EDD2020 import getBBoxCordinatesFromMask_yolo
#, getBBoxCordinatesFromMask_voc

def rectangle(height, width, c0, r0 ):
    rr, cc = [r0, r0 + width, r0 + width, r0], [c0, c0, c0 + height, c0 + height]
    return skimage.draw.polygon(rr, cc)

def maskImage_EDD2020(maskFolder, categoryList, fileList, dataset_dir, classCategory,shapeFormat, segy, segx, circ, rect, debugLevel=1):
    fileCounter = 0
    os.makedirs(maskFolder, exist_ok='True')
    
    for ll in range (0, len(fileList)):
        print(ll)
        image_path = os.path.join(dataset_dir, fileList[ll])
        image = io.imread(image_path)
        height, width = image.shape[:2]
        mask = np.zeros([height, width, len(categoryList)], dtype=np.uint8)
        img = np.zeros([height, width, 3], dtype=np.uint8)
        cnt = 0
        cnt_p=0
        cnt_r = 0
        
        if (fileCounter <10):
            newFileName = 'EDD2020_sample000'+str(fileCounter)
        elif (fileCounter <100):
            newFileName = 'EDD2020_sample00'+str(fileCounter)
        elif (fileCounter <1000):
            newFileName = 'EDD2020_sample'+str(fileCounter)
        
        txt_path=os.path.join(maskFolder, newFileName+'.txt')
        for i in range (0, len(shapeFormat[ll])):
            if shapeFormat[ll][i]== 'polyline':
                if debugLevel:
                    print('we are dealing with polyline')
                rr, cc = skimage.draw.polygon(segy[ll][cnt_p], segx[ll][cnt_p])
                rr = np.clip(rr, 0, height-1)
                cc = np.clip(cc, 0, width-1) 
                cnt_p = cnt_p + 1
        
            elif shapeFormat[ll][i]== 'polygon':
                if debugLevel:
                    print('we are dealing polygon')
                
                rr, cc = skimage.draw.polygon(segy[ll][cnt_p], segx[ll][cnt_p])
                rr = np.clip(rr, 0, height-1)
                cc = np.clip(cc, 0, width-1)              
                cnt_p = cnt_p + 1
    
            elif shapeFormat[ll][i]== 'circle':
                if debugLevel:
                    print('we are dealing with circle')
                rr, cc = skimage.draw.circle(circ[ll][cnt][1], circ[ll][cnt][0], circ[ll][cnt][2])
                rr = np.clip(rr, 0, height-1)
                cc = np.clip(cc, 0, width-1) 
                cnt = cnt +1
                
            elif shapeFormat[ll][i]== 'rect':
                if debugLevel:
                    print('we are dealing with rectangle')
                rr, cc = rectangle(rect[ll][cnt_r][1], rect[ll][cnt_r][0], rect[ll][cnt_r][2],rect[ll][cnt_r][3] )
                rr = np.clip(rr, 0, height-1)
                cc = np.clip(cc, 0, width-1)
                cnt_r = cnt_r+1
    
            if (classCategory[ll][i]) == []:
                print('empty')
            else:
                mask[rr,cc, int(classCategory[ll][i][0])] = 255
                mask2 = np.zeros([height, width], dtype=np.uint8)
                mask2[rr,cc] = 255
#                img = getBBoxCordinatesFromMask_voc(image, mask2, txt_path, categoryList[int(classCategory[ll][i][0])], int(classCategory[ll][i][0]))
                img = getBBoxCordinatesFromMask_yolo(image, mask2, txt_path, categoryList[int(classCategory[ll][i][0])], int(classCategory[ll][i][0]), width, height) 
                
        im_mask = mask.transpose([2,0,1])    
        imsave(os.path.join(maskFolder,newFileName+'_mask.tif'), im_mask)
    
        # loop for channel wise:
        for i in range (0, len(categoryList)):
            if np.sum(im_mask[i,:,:])!=0:
                imsave(os.path.join(maskFolder, newFileName+'_'+categoryList[i]+'.tif'), im_mask[i,:,:]) 
                
        imsave(os.path.join(maskFolder, newFileName+'_bbox'+'.png'),img) 
        shutil.copy(image_path, os.path.join(maskFolder, newFileName+'.jpg'))
        fileCounter=fileCounter+1
        
        


        
