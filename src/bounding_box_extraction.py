#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 20:18:23 2018
@author: shaun
@Description: Script select regions of interest and assign categories
"""
import cv2
import configparser
import numpy as np
import pickle
from PIL import Image
from matplotlib.pyplot import imshow, show, matshow
import os
%matplotlib inline

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
    # Application configuration                                   #
    ###############################################################

    # Read images
    images = ["video_conversion/024_Above_0.jpg", "video_conversion/024_Above_1.jpg"]

    for image in images:
        # 
        im = cv2.imread(image)
        r = cv2.selectROIs("Image", im, fromCenter=False, showCrosshair=False)
        cv2.destroyAllWindows()

        if r.size != 0:
            co_ord_class = {}
            for i in range(0, len(r)):
                x1 = r[i][0]
                y1 = r[i][1]
                x2 = x1 + r[i][2]
                y2 = y1 + r[i][3]

                p = Image.fromarray(im[y1:y2, x1:x2])
                imshow(p)
                show()

                img_class = input('Enter class for co-ordinates %s:' % (r[i]))
                co_ord_class.update({i: {'coords': r[i], 'class': img_class}})

            roi_dict.update({image: co_ord_class})

        pickle.dump(roi_dict, open('./image_rois.p', 'wb'))
