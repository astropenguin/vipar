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
from viparc.utils import default, go, inp

# definition of task
def mbinit(version, status):
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    if not '__mbscans__' in mbglobals.keys():
        mbglobals['__mbscans__'] = ViparDB()

    if not '__mbmaps__' in mbglobals.keys():
        mbglobals['__mbmaps__'] = ViparDB()

    if not incasa:
        mbglobals['default'] = default
        mbglobals['go'] = go
        mbglobals['inp'] = inp

    logger.post('Vipar - version {0} ({1})'.format(version, status))
    logger.post('initial settings of Vipar finished')
