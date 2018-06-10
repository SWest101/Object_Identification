#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 20:18:23 2018
@author: shaun
@Description: Script to convert videos to into frames
"""
import argparse
import cv2
import os


def directory_check(path):
    '''
    Description: Function to check if path exists and to create it if it
                does not.
    Arguments: path - String
    Return:
    '''
    # Check if path does not exist then create it
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            raise ValueError(e)


def video_frame_extractor(video_input_path, output_path):
    '''
    Description: Function to extract videos into frames
    Arguments:  video_input_path - String of video location
                output_path - String of image frame output location
    Return:
    '''

    # Check if the output directory exists and create it it doesn't
    directory_check(output_path)

    # Create a VideoCapture object of the specified video
    vid = cv2.VideoCapture(video_input_path)

    # Read the video file to see if it can be opened
    success, image = vid.read()

    # Split the video path into it's directory path, file type and name
    vid_path, vid_ext = os.path.splitext(video_input_path)
    vid_dir, vid_name = os.path.split(vid_path)

    # Intializing looping variables
    count = 0
    success = True

    # Write the frame to the designated path and test if it was written
    # successfully. Exit loop if it did not
    while success:
        cv2.imwrite("%s/%s_%s.jpg" % (output_path, vid_name, count), image)
        success, image = vid.read()
        count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process video into frames')
    parser.add_argument('--video',
                        type=str,
                        required=True,
                        help='Path to the video to be converted')

    parser.add_argument('--output-path',
                        type=str,
                        required=True,
                        help='Path to where the video frames are to saved')

    args = parser.parse_args()

    result = video_frame_extractor(video_input_path=vars(args)['video'],
                                   output_path=vars(args)['output_path'])

    print('Video conversion successful')
