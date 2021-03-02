#!/bin/env python3

"""
Find repetitions in a corpus of video files
"""

import sys
import argparse
from video_repetitions import read_videos

parser = argparse.ArgumentParser(description = "Check repetitions in a corpus of video files")
parser.add_argument("-i", "--input", nargs= '*', metavar = "path", type = str, \
                    help = "Video files names separated by spaces.")
parser.add_argument("-o", "--output", metavar = "output_file", type = str, \
                    default = sys.stdout, \
                    help = "Outputs results in specified file. Defaults to standard output.")
parser.add_argument("-m", "--method", metavar = "method", type = str, \
                    default = 'average', \
                    help = "Method to compare video frames.")
parser.add_argument("-p", "--period", metavar = "minimum_repetion_period", \
                    type = int, default = 24, \
                    help = "Minimum period for a meaningful repetition.")

args = parser.parse_args()

if len(args.input) == 0:
    sys.exit(1)

# print(args.input)
# print(args.output)
# print(args.method)
# print(args.period)

result = read_videos(args.input, method=args.method, repetitions_period=args.period, verbose=True)
for filename in result:
    print(filename, ':', file=args.output)
    for start, end in result[filename]:
        print(start, '-', end, file=args.output)
