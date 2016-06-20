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

# definition of task
def mbsavemap(fitsname, label=''):
    taskname = sys._getframe().f_code.co_name
    mbglobals = sys._getframe(len(inspect.stack())-1).f_globals
    logger.origin(taskname)
    logger.post('not implemented yet!')
