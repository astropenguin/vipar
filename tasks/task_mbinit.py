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
from viparc.data import ViparDB

# definition of task
def mbinit():
    taskname = sys._getframe().f_code.co_name
    mbglobals = sys._getframe(len(inspect.stack())-1).f_globals
    logger.origin(taskname)

    if not '__mbscans__' in mbglobals.keys():
        mbglobals['__mbscans__'] = ViparDB()

    if not '__mbmaps__' in mbglobals.keys():
        mbglobals['__mbmaps__'] = ViparDB()

    logger.post('Vipar - release 0.1.3 (alpha)')
    logger.post('initial settings of Vipar finished')
