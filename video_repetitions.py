#!/bin/env python3
"""
CLI python tool to create movies out of an anime arc
"""

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
    print('{}%\r'.format(percentage), end='')


def read_videos(files, repetitions_period=MINIMUM_PERIOD, verbose=False):
    """
    read_videos
    :param files: path to files. Episodes are expected to be in order
    :param repetitions_period: minimum period of a meaningful repetition
    :param verbose: should the function print output or not
    :return: list of pairs (start, end) file that flag a frame repetition for each filename
    """
    frames_dicts = []
    flags = {}
    for filename in files:
        flags[filename] = read_video(filename, frames_dicts, repetitions_period, verbose)
    return flags

def read_video(filename, frames_dicts=None, repetitions_period=MINIMUM_PERIOD, verbose=False):
    """
    read_videos
    :param filename: path to file
    :param frames_dict: lists of episodes' dictionary of frames. Defaults to []
    :param repetitions_period: minimum period of a meaningful repetition. Defaults to 1 second
    :param verbose: should the function print output or not
    :return: list of pairs (start, end) that flag a frame repetition in filename
    """
    if frames_dicts is None:
        frames_dicts = []
    my_dict = {}
    log("Reading video file {}...".format(filename), verbose)
    vidcap = cv.VideoCapture(filename)
    total_frames = int(vidcap.get(cv.CAP_PROP_FRAME_COUNT))
    success, image = vidcap.read()
    count = 0
    matched = False # After the first match is hit, the state alternates between match and not match
    flags = []
    while success:
        my_hash = imagehash.average_hash(Image.fromarray(image, 'RGB'))
        # my_hash = hash(str(image.data))
        # my_hash = hash(image.tobytes())
        # Adding frame information
        if my_hash in my_dict:
            my_dict[my_hash].append(count)
        else:
            my_dict[my_hash] = [count]
        # Only check previous episodes frames
        if len(frames_dicts) > 0 and any(my_hash in x for x in frames_dicts):
            if matched:
                start, _ = flags[-1]
                flags[-1] = (start, count)
            else:
                flags.append((count, count))
            matched = True
        else:
            # Check that last entry is "long" enough to be meaningful
            if len(flags) > 0:
                start, end = flags[-1]
                if end - start < repetitions_period:
                    flags.pop(-1)
            matched = False
        success, image = vidcap.read()
        count += 1
        if verbose:
            update_progress(count, total_frames)
    # start, _ = flags[-1]
    # flags[-1] = (start, total_frames)
    frames_dicts.append(my_dict)
    log("Done  ", verbose)
    return flags
