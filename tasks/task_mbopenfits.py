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
from viparc.data import MBScan

# definition of task
def mbopenfits(mbfits, mode='readonly', memmap=False):
    taskname = sys._getframe().f_code.co_name
    mbglobals = sys._getframe(len(inspect.stack())-1).f_globals
    logger.origin(taskname)

    fitsname = os.path.basename(mbfits)
    logger.post('MBFITS: {}'.format(fitsname))

    try:
        f = fits.open(mbfits, mode, memmap)
        logger.post('MBFITS is successfully opened')
    except:
        logger.post('an error occured', 'ERROR')

    mbsc = MBScan.fromfits(f)
    mbsc.recordtask(taskname)

    if '__mbfits__' in mbglobals.keys():
        mbglobals['__mbfits__'].close()
        del mbglobals['__mbfits__']

    mbglobals['__mbfits__'] = f
    mbglobals['__mbscans__'].append(mbsc)

    logger.post('MBFITS is now stored as __mbfits__')
    logger.post('MBScan is now stored as __mbscans__[0]')
