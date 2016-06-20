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
def mblistmap():
    taskname = sys._getframe().f_code.co_name
    mbglobals = sys._getframe(len(inspect.stack())-1).f_globals
    logger.origin(taskname)

    mbmps = mbglobals['__mbmaps__']
    keys_history = sorted([key for key in mbmps.keys() if type(key) == int])
    keys_pin = sorted([key for key in mbmps.keys() if type(key) == str])
    textcases = lambda N: '{} {}'.format(N, ['map is', 'maps are'][N>1])

    # list scan(s) in history
    logger.post('{} stored as history:'.format(textcases(len(keys_history))))
    logger.post('')
    for key in keys_history:
        hd = mbmps[key]['data'].header
        logger.post('label: {} {}'.format(key, '(latest)'*(key==0)))
        logger.post('- shape: {} grid x {} grid'.format(hd['NAXIS1'], hd['NAXIS2']))
        logger.post('- origin: {}'.format(hd['ORIGIN']))
        logger.post('- taskflow: {}'.format(hd['TASKFLOW']))
        logger.post('')

    # list pinned scan(s)
    logger.post('{} pinned:'.format(textcases(len(keys_pin))))
    logger.post('')
    for key in keys_pin:
        hd = mbmps[key]['data'].header
        logger.post("label: '{}'".format(key))
        logger.post('- shape: {} grid x {} grid'.format(hd['NAXIS1'], hd['NAXIS2']))
        logger.post('- origin: {}'.format(hd['ORIGIN']))
        logger.post('- taskflow: {}'.format(hd['TASKFLOW']))
        logger.post('')
