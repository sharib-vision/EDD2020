#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 15:34:14 2020

@author: shariba
"""
import matplotlib.pyplot as plt
import numpy as np


def show_images(images, cols = 2, titles = None):
    assert((titles is None)or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1,n_images + 1)]
    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
    plt.show()


def inputImageViz (inputImage, gt_mask_concatinated):
    show_images(gt_mask_concatinated[0,:, :,:]) 
    plt.imshow(np.transpose(inputImage[0,:, :,:], axes=[1, 2, 0]) )
    plt.show()