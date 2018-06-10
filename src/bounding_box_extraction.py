#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 20:18:23 2018
@author: shaun
@Description: Script select regions of interest and assign categories to them.
              The ROIs are then saved to a pickle file to be used in further
              training.
"""
import argparse
import cv2
import configparser
import numpy as np
import pickle
import glob
from PIL import Image
from matplotlib.pyplot import imshow, show, matshow
import os
%matplotlib inline


def image_check(new_image_name, old_image_list, comparison):
    '''Description: Function to check if an image has already been processed
                    and has labels assigned to it.
      Arguments: new_image_list - List of all images
                 old_image_list - List of names already existing
                 comparison - String indicating the comparison between two lists
                              to be performed
      Return: image_list - List of required elements
    '''


def images_in_directory(directory):
    '''Description: Function to obtain a list of images in a directory
      Arguments: directory - String of image directory to find images in
      Return: images_list - List of image filenames
    '''
    images_list = []
    for filename in glob.iglob(directory + '/**/*', recursive=True):
        if filename.lower().endswith(('.jpg', '.png', '.gif')):
            try:
                img = Image.open(filename)
                # verify that file is an image
                img.verify()
                images_list.append(filename)
            except:
                print(filename + ' is not an image')

    return images_list


if __name__ == '__main__' :

    ###############################################################
    # Application configuration                                   #
    ###############################################################
    # Read config file where the image classes and URL are contained.
    config = configparser.ConfigParser()
    try:
        config.read('./config.ini')
    except Exception as e:
        raise ValueError(e)

    # File paths
    roi_path = config.get('REGIONS_OF_INTEREST', 'image_roi')

    if os.path.exists(roi_path):
        roi_dict = pickle.load(open(roi_path, "rb"))
    else:
        roi_dict = {}

    ###############################################################
    # Parse CMD arguments                                         #
    ###############################################################

    parser = argparse.ArgumentParser(description='Selection of regions of interest from images')
    parser.add_argument('--image_dir',
                        type=str,
                        required=True,
                        help='Path to the images to be processed')

    parser.add_argument('--process',
                        type=str,
                        required=False,
                        default='new',
                        choices=['all', 'new', 'existing'],
                        help='Flag to indicate if all, new or existing images should be processed [Default: new]')

    args = parser.parse_args()

    image_dir = vars(args)['image_dir']
    process = vars(args)['process']

    ###############################################################
    # Obtain list of images                                       #
    ###############################################################

    images_list = images_in_directory(image_dir)
    if not images_list:
        raise ValueError("There are no images to process in " + image_dir)

    # if dictionary object is not empty
    if roi_dict:
        images = image_check(images_list, [key for key in roi_dict.keys()], process)

    for image in images:
        # This will return a 3D numpy array of the dimensions of the image
        im = cv2.imread(image)

        # Use contribution library to select multiple ROIs
        # This returns a numpy array of ROIs [x1, y1, x2-x1, y2-y1]
        r = cv2.selectROIs("Image", im, fromCenter=False, showCrosshair=False)
        cv2.destroyAllWindows()

        # If 
        if r.size != 0:
            co_ord_class = {}
            for i in range(0, len(r)):
                x1 = r[i][0]
                y1 = r[i][1]
                x2 = x1 + r[i][2]
                y2 = y1 + r[i][3]

                # create image from array to be displayed inline
                p = Image.fromarray(im[y1:y2, x1:x2])
                imshow(p)
                show()

                # Require input from user to assign class of ROI
                img_class = input('Enter class for co-ordinates %s:' % (r[i]))
                co_ord_class.update({i: {'coords': r[i], 'class': img_class}})

            roi_dict.update({image: co_ord_class})

        pickle.dump(roi_dict, open('./image_rois.p', 'wb'))
