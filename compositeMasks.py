#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 11:00:22 2020

@author: shariba
"""


def get_args():
    
    import argparse
    parser = argparse.ArgumentParser(description="For EAD2019 challenge: semantic segmentation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # test data
    parser.add_argument("--maskDir", type=str, default="./annotations/phase-II-200frames/BB_200_annotations_all/masks", help="ground truth single channel image (to 5 channel tif image only)")
    parser.add_argument("--orginalImageDir", type=str, default="./annotations/phase-II-200frames/BB_200_annotations_all/original", help="original image")
    parser.add_argument("--compositeImageDir", type=str, default="././annotations/phase-II-200frames/BB_200_annotations_all/compositeMasks/", help="combined tiff")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    import tifffile as tiff
    from tifffile import imsave
    import cv2
    import numpy as np
    import glob
    import os
    
    args = get_args()
    
    os.makedirs(args.compositeImageDir, exist_ok=True)
    
    categoryList = ['BE', 'suspicious', 'HGD' , 'cancer', 'polyp']
    
    ext = ['*.jpg']
    for filename in sorted(glob.glob(args.orginalImageDir + '/'+ ext[0], recursive = True)):
        file=filename.split('/')[-1]
        fileNameOnly = file.split('.')[0]
        nClasses_annotated = len(glob.glob1(args.maskDir,fileNameOnly+"*.tif"))
        fileList = glob.glob1(args.maskDir,fileNameOnly+"*.tif")
       
        # read original and make stack of mask images
        image = cv2.imread(filename)
        height, width = image.shape[:2]
        mask = np.zeros([height, width, len(categoryList)], dtype=np.uint8)
        
        for i in range (0, nClasses_annotated):
            f = fileList[i].split('_')[-1]
            if f.split('.')[0] == 'BE':
                mask[:,:, 0] = tiff.imread(os.path.join(args.maskDir,fileList[i]))
            elif (f.split('.')[0]== 'suspicious'):
                mask[:,:, 1] = tiff.imread(os.path.join(args.maskDir,fileList[i]))
            elif (f.split('.')[0] == 'HGD'):
                mask[:,:, 2] = tiff.imread(os.path.join(args.maskDir,fileList[i]))
            elif (f.split('.')[0] == 'cancer'):
                mask[:,:, 3] = tiff.imread(os.path.join(args.maskDir,fileList[i]))
            elif (f.split('.')[0] == 'polyp'):
                mask[:,:, 4] = tiff.imread(os.path.join(args.maskDir,fileList[i]))
                
                
            im_mask = mask.transpose([2,0,1])    
            imsave(os.path.join(args.compositeImageDir,fileNameOnly+'_mask.tif'), im_mask)      
            