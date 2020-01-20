#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 11:06:33 2020

@author: shariba
"""

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description="For EDD202 challenge", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dataset_dir", type=str, default="../annotations/samples/", help="ground truth mask image and prints (5 channel tif image only)")
    parser.add_argument("--via_annotationFile", type=str, default="../json/via_sample_EDD2020.json", help="sample json file")
    parser.add_argument("--classLabels", type=str, default="../class_list.txt", help="class labels")
    parser.add_argument("--maskFolder_Results", type=str, default="../masks/", help="mask image aggregated, separate, bbox, png bbox overlay")
    args = parser.parse_args()
    return args

# read txt files
def classList (filepath):
    classList = []
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            print("Line {}: {}".format(cnt, line))
            classList.append(line.split('\n')[0])
    return classList
    
def json2shapes(via_annotationFile, categoryList):
    import json
    segment=[]
    fileList=[]  
    with open(via_annotationFile) as json_data:
        data = json.load(json_data)
        for p in data["_via_img_metadata"].values():
            print(p)
            if len(p['regions'])!=0:
                fileList.append(p['filename'])
                segment.append(p['regions'])
    shapeFormat=[]
    classCategory = []
    segx = []
    segy = []
    rect = []
    circ=[]
    debugLevel = 1
    for i in range (0, len(segment)):
        seg = segment[i]
        
        shapeFormat_1=[]
        classCategory_1 = []
        segx_1 = []
        segy_1 = []
        rect_1 = []
        circ_1=[]
        
        for k in range (0, len(seg)):
            seg_1 = seg[k]
            seg2 = seg_1['region_attributes']
            seg1 = seg_1['shape_attributes']  
            seg1_category = seg2['DiseaseGrading']
            new_category = {}
            if len(seg1_category) < 6 or len(seg1_category) == 0:
                for i in range (0, len(categoryList)):
                    for key in seg1_category.keys():
                        print(key)
                        if key != categoryList[i]:
                            new_category[categoryList[i]]= False
                        else:
                            new_category[categoryList[i]]=True
            seg1_category = new_category
        
            listBoolCat = list(seg1_category.values())
            
            x = {k:v for k,v in enumerate(listBoolCat) if v == True}
            classCategory_1.append(list(x))
            # for shape identification
            shapesArray=['polygon', 'polyline', 'circle', 'rect']
            seg2_shape = seg1['name']  
            
            if seg2_shape == shapesArray[1]:
                if debugLevel:
                    print('polyline exists')
                shapeFormat_1.append(seg2_shape)
                segx_1.append(seg1['all_points_x'])
                segy_1.append(seg1['all_points_y'])
                
            elif seg2_shape == shapesArray[0]:
                if debugLevel:
                    print('polygon exists')
                shapeFormat_1.append(seg2_shape)
                segx_1.append(seg1['all_points_x'])
                segy_1.append(seg1['all_points_y'])
                
            elif seg2_shape == shapesArray[2]:
                circleRegion=[]
                if debugLevel:
                    print('circle exists')
                shapeFormat_1.append(seg2_shape)
                circleRegion.append(int(seg1['cx']))
                circleRegion.append(int(seg1['cy']))
                circleRegion.append(int(seg1['r']))
                circ_1.append(circleRegion)
                
            elif seg2_shape == shapesArray[3]:
                if debugLevel:
                    print('rectangle exists')
                rectangleCoordinates=[]
                shapeFormat_1.append(seg2_shape)
                rectangleCoordinates.append(int(seg1['height']))
                rectangleCoordinates.append(int(seg1['width']))
                rectangleCoordinates.append(int(seg1['x']))
                rectangleCoordinates.append(int(seg1['y']))
                rect_1.append(rectangleCoordinates)
                
            else:
                print('unidentified')
                
        shapeFormat.append(shapeFormat_1)
        classCategory.append(classCategory_1)
        segx.append(segx_1)
        segy.append(segy_1)
        rect.append(rect_1)
        circ.append(circ_1)
    classCategory = list(filter(None, classCategory))
    shapeFormat = list(filter(None, shapeFormat))
    return fileList, shapeFormat, classCategory, segx, segy, rect, circ

if __name__ == '__main__':
    
    from maskImageFunctions_EDD import maskImage_EDD2020
    args_EDD2020 = get_args()
    dataset_dir = args_EDD2020.dataset_dir
    via_annotationFile = args_EDD2020.via_annotationFile
    maskFolder = args_EDD2020.maskFolder_Results
    #============== get class-labels ==============
    txfFile  = args_EDD2020.classLabels
    cLabels = classList (txfFile)
    #============== function calls ==============
    fileList, shapeFormat, classCategory, segx, segy, rect, circ = json2shapes(via_annotationFile, cLabels)
    #============== generate mask-images/overlay-images/bboxes ==============
    maskImage_EDD2020(maskFolder, cLabels, fileList, dataset_dir, classCategory,shapeFormat, segy, segx, circ, rect, debugLevel=1)

    