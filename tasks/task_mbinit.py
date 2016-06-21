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
from viparc.data import ViparDB

# definition of task
def mbinit():
    depth = len(inspect.stack())-1 if incasa else 1
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    if not '__mbscans__' in mbglobals.keys():
        mbglobals['__mbscans__'] = ViparDB()

    if not '__mbmaps__' in mbglobals.keys():
        mbglobals['__mbmaps__'] = ViparDB()

    logger.post('Vipar - release 0.2.1 (alpha)')
    logger.post('initial settings of Vipar finished')
