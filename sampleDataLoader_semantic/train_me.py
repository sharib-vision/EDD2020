#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:24:45 2020

@author: shariba
"""

def get_args():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-e', '--epochs', dest='epochs', default=1, type='int',
                      help='number of epochs')
    parser.add_option('-b', '--batch_size', dest='batchsize', default=1,
                      type='int', help='batch size')
    parser.add_option('-l', '--learning-rate', dest='lr', default=0.1,
                      type='float', help='learning rate')
    parser.add_option('-g', '--gpu', action='store_true', dest='gpu',
                      default=False, help='use cuda')
    parser.add_option('-c', '--load', dest='load',
                      default=False, help='load file model')
    # input settings
    parser.add_option('-m', '--mask_Dir', dest='masks', default='data/train_masks/',
                      type='str', help='base direcotry for masks ')
    parser.add_option('-i', '--image_Dir', dest='images', default='data/train_images/',
                      type='str', help='base direcotry for images ')
    parser.add_option('-w', '--maxWidth', dest='maxWidth', default=512,
                      type='int', help='max image width (to be resized if not same)') 
    parser.add_option('-z', '--maxHeight', dest='maxHeight', default=512,
                      type='int', help='max image height (to be resized if not same)') 
    parser.add_option('-s', '--scale', dest='scale', type='float',
                      default=0.5, help='downscaling factor of the images')
    parser.add_option('-v', '--val_percent', dest='valpercent', type='float',
                      default=0.1, help='validation percentage for splitting')
    parser.add_option('-n', '--n_classes', dest='classes', default=5,
                      type='int', help='number of class labels')

    (options, args) = parser.parse_args()
    return options


if __name__ == '__main__':
    import numpy as np
    from utils import split_train_val, batch, get_imgs_and_masks, inputImageViz
    # get all values that you require from your input
    args = get_args()    
    dir_img = args.images
    dir_mask = args.masks
    dir_checkpoint = 'checkpoints/'
    
    val_percent = args.valpercent
    scale = args.scale
    maxWidth = args.maxWidth
    maxHeight = args.maxHeight
    n_classes= args.classes
    
    iddataset = split_train_val(dir_img, val_percent)
    
    train = get_imgs_and_masks(iddataset['train'], dir_img, dir_mask, scale, maxWidth, maxHeight, n_classes)
    val = get_imgs_and_masks(iddataset['val'], dir_img, dir_mask, scale, maxWidth, maxHeight, n_classes)

    for epoch in range(args.epochs):
        print('Starting epoch {}/{}.'.format(epoch + 1, epochs))
        #net.train()
        for i, k in enumerate(batch(val, args.batchsize)):
            print(i)
            imgs = np.array([i[0] for i in k]).astype(np.float32)
            true_masks = np.array([i[1] for i in k])
            # comment this if required
            inputImageViz (imgs, true_masks)
            #------------ your training code here!!!--------------------
        
        
        
        
        #-----------------------------------------------------------