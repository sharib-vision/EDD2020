#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:27:33 2020

@author: shariba
"""
import os
import random
import numpy as np
from PIL import Image
import tifffile as tiff

from .utils import get_square, resize_and_crop, normalize, hwc_to_chw

def resize_and_crop_mask(tiffImage, w=512, h=512, classes=5,  scale=0.5, final_height=None):
    newW = int(w * scale)
    newH = int(h * scale)
    if not final_height:
        diff = 0
    else:
        diff = newH - final_height
    img_tiff = tiff.imread(tiffImage)/255
    
    newImg = np.zeros([newW, newH, classes], dtype=np.uint8)
    for i in range(0, classes):
        img =  Image.fromarray(np.uint8(img_tiff[i,:,:]))
        img_resize = img.resize((newW, newH))
        img_resize = img_resize.crop((0, diff // 2, newW, newH - diff // 2))
        newImg[:,:, i] = np.array(img_resize, dtype=np.uint8)
    return np.array(newImg, dtype=np.uint8)

def get_ids(dir):
    return (f[:-4] for f in os.listdir(dir))

def split_ids(ids, n=2):
    return ((id, i)  for id in ids for i in range(n))

def split_train_val(dir, val_percent=0.05):
    ids = get_ids(dir)
    ids = split_ids(ids, n=1)
    samples = list(ids)
    length = len(samples)
    n = int(length * val_percent)
    random.shuffle(samples)
    return {'train': samples[:-n], 'val': samples[-n:]}

def to_cropped_imgs(ids, dir, suffix, scale, maxWidth=512, maxHeight=512):
    for id, pos in ids:
        im = resize_and_crop(Image.open(dir + id + suffix), maxWidth, maxHeight,scale=scale)
        yield get_square(im, pos)
        
def to_cropped_imgs_mask(ids, dir, suffix, scale, maxWidth=512, maxHeight=512, n_classes=5): 
    for id, pos in ids:
        im = resize_and_crop_mask(dir + id + suffix,  maxWidth, maxHeight, n_classes, scale=scale)
        yield get_square(im, pos)
        
def get_imgs_and_masks(ids, dir_img, dir_mask, scale, maxWidth, maxHeight, n_classes):
    imgs = to_cropped_imgs(ids, dir_img, '.jpg', scale, maxWidth, maxHeight)
    imgs_switched = map(hwc_to_chw, imgs)
    imgs_normalized = map(normalize, imgs_switched)
    masks = to_cropped_imgs_mask(ids, dir_mask, '_mask.tif', scale, maxWidth, maxHeight, n_classes)
    masks_switched = map(hwc_to_chw, masks)
    return zip(imgs_normalized, masks_switched)

