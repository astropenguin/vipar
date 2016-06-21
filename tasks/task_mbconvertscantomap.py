# coding: utf-8

# common preamble
import os
import sys
import inspect
import numpy as np
root = os.path.dirname(__file__)
sys.path.append('{0}/../'.format(root))
incasa = '__CASAPY_PYTHONDIR' in os.environ
if incasa:
    from taskinit import casalog as logger
else:
    from viparc.log import pythonlog as logger

# unique preamble
import pyfits as fits
from viparc.map import SinglePixel

# definition of task
def mbconvertscantomap(method='singlepixel', gridsize=[6,6], gridrefval=[0,0], label='', pixel=None):
    depth = len(inspect.stack())-1 if incasa else 1
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbsc = mbglobals['__mbscans__'][label]

    if method == 'singlepixel':
        converter = SinglePixel(pixel, gridsize, gridrefval)
        logger.post('method: single pixel')
        logger.post('pixel to be processed: {0}'.format(pixel))

    mbmp = mbsc.tomap(converter)
    mbmp.recordtask(taskname)
    mbglobals['__mbmaps__'].append(mbmp)

    logger.post('map is successfully converted from MBScan')
    logger.post('new MBMap is now stored as __mbmaps__[0]')
