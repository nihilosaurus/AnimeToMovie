#!/bin/env python3

"""
Tests cases
"""

from video_repetitions import read_videos

def do_test(name, value):
    """
    Do test
    """
    passed = 'PASSED' if value else 'FAILED'
    print(name, '[', passed, ']')

def test_1():
    """
    Testing that openings are detected
    """
    files = []
    files.append('Hard_Corner-Skyrim_Edition_Collector.mp4')
    files.append('Hard_Corner-Special_Berserk.mp4')
    checks = []
    checks.append(1080)
    checks.append(1392)
    output = read_videos(files)
    result = False
    for file_object, check in zip(files, checks):
        for start, end in output[file_object]:
            if start <= check <= end:
                result = True
                break
    return result


TESTS = {
    'Opening detection from repetitions': test_1()
}


if __name__ == "__main__":
    for test in TESTS:
        do_test(test, TESTS[test])
