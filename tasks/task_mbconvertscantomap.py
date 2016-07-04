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
from viparc.map import DefaultConverter, PointingConverter

# definition of task
def mbconvertscantomap(method='default', rcpfile=None, pixels=[], gain='point', pixel=None, gridsizes=[6.0,6.0], gridrefvals=[0.0,0.0], label=''):
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbsc = mbglobals['__mbscans__'][label]

    if method == 'default':
        rcpfile = os.path.expanduser(rcpfile)
        converter = DefaultConverter(rcpfile, pixels, gain, gridsizes, gridrefvals)
        logger.post('method: default')
        logger.post('RCP: {0}'.format(os.path.basename(rcpfile)))
    elif method == 'pointing':
        converter = PointingConverter(pixel, gridsizes, gridrefvals)
        logger.post('method: pointing')
        logger.post('pixel to be processed: {0}'.format(pixel))

    mbmp = mbsc.tomap(converter)
    mbmp.recordtask(taskname)
    mbglobals['__mbmaps__'].append(mbmp)

    logger.post('map is successfully converted from MBScan')
    logger.post('new MBMap is now stored as __mbmaps__[0]')
