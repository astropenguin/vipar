# coding: utf-8

# common preamble
import os
import sys
import inspect
import numpy as np
root = os.path.dirname(__file__)
sys.path.append('{}/../'.format(root))
try:
    from taskinit import casalog as logger
except ImportError:
    from viparc.log import pythonlog as logger

# unique preamble
import pyfits as fits
from viparc.map import SinglePixel

# definition of task
def mbconvertscantomap(method='singlepixel', gridsize=[6,6], gridrefval=[0,0], label='', pixel=None):
    taskname = sys._getframe().f_code.co_name
    mbglobals = sys._getframe(len(inspect.stack())-1).f_globals
    logger.origin(taskname)

    mbsc = mbglobals['__mbscans__'][label]

    if method == 'singlepixel':
        converter = SinglePixel(pixel, gridsize, gridrefval)
        logger.post('method: single pixel')
        logger.post('pixel to be processed: {}'.format(pixel))

    mbmp = mbsc.tomap(converter)
    mbmp.recordtask(taskname)
    mbglobals['__mbmaps__'].append(mbmp)

    logger.post('map is successfully converted from MBScan')
    logger.post('new MBMap is now stored as __mbmaps__[0]')
