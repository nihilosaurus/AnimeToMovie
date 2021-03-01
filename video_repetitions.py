#!/bin/env python3
"""
CLI python tool to create movies out of an anime arc
"""

import sys
# import numpy as np
import cv2 as cv
import imagehash
from PIL import Image

TEST_1 = 'Skyrim+Edition+Collector+ +Hard+Corner+(Benzaie).mp4'
TEST_2 = 'Special+BERSERK+-+Hard+Corner+(Benzaie).mp4'
FRAMES_DICT = {}
FLAGS = {}

MINIMUM_PERIOD = 24

def log(string, boolean):
    """
    print or not
    """
    if boolean:
        print(string)

def update_progress(progress, total):
    """
    progress percentage
    """
    percentage = round(progress/total*100, 0)
    sys.stdout.write('{}%\r'.format(percentage))
    sys.stdout.flush()


def read_videos(files, repetitions_period=MINIMUM_PERIOD, verbose=False):
    """
    read_videos
    """
    for file_object in files:
        read_video(file_object, repetitions_period, verbose)
    return FLAGS

def read_video(filename, repetitions_period=MINIMUM_PERIOD, verbose=False):
    """
    read_videos
    """
    log("Reading video file {}...".format(filename), verbose)
    vidcap = cv.VideoCapture(filename)
    total_frames = int(vidcap.get(cv.CAP_PROP_FRAME_COUNT))
    success, image = vidcap.read()
    count = 0
    first = True # Not Matched Yet state
    matched = False # After the first match is hit, the state alternates between match and not match
    while success:
        my_hash = imagehash.average_hash(Image.fromarray(image, 'RGB'))
        # my_hash = hash(str(image.data))
        # my_hash = hash(image.tobytes())
        if my_hash in FRAMES_DICT:
            FRAMES_DICT[my_hash].append((filename, count))
            if first:
                # for the first match
                FLAGS[filename] = [(count, count)]
                first = False
            else:
                if matched:
                    start, _ = FLAGS[filename][-1]
                    FLAGS[filename][-1] = (start, count)
                else:
                    FLAGS[filename].append((count, count))
            # if not matched:
            #     print("Match!")
            matched = True
        else:
            FRAMES_DICT[my_hash] = [(filename, count)]
            # check that last entry is "long" enough to be meaningful
            if filename in FLAGS and len(FLAGS[filename]) > 1:
                start, end = FLAGS[filename][-1]
                if end - start < repetitions_period:
                    FLAGS[filename].pop(-1)
            # if matched:
            #     print("Unmatch...")
            matched = False
        success, image = vidcap.read()
        # if not count%1000:
        #     print(count)
        count += 1
        if verbose:
            update_progress(count, total_frames)
    start, _ = FLAGS[filename][-1]
    FLAGS[filename][-1] = (start, total_frames)
    log("Done  ", verbose)
