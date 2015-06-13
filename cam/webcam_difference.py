#!/usr/bin/env python
from __future__ import division

"""
Simple module to check the algorithm to difference 
"""

__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'


import cv2
import sys
import math
import os


def diffImg(t0, t1):
    print t0
    print 'eeeeeeee'
    print t1
    dif = cv2.absdiff(t0, t1).sum()
    ncomponents = len(t0[0]) * len(t0)
    return (dif / 254.0 * 100) / ncomponents


def main(argv=None):

    white = cv2.imread('white.jpg')
    black = cv2.imread('black.jpg')
    whiteGray = cv2.cvtColor(white, cv2.COLOR_BGR2GRAY)
    blackGray = cv2.cvtColor(black, cv2.COLOR_BGR2GRAY)

    percent_difference = diffImg(whiteGray, blackGray)
    sys.stdout.flush() 
    print "percentatge: " + str(percent_difference)

    return

if __name__ == "__main__":
    sys.exit(main())

