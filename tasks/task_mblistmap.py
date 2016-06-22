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

# definition of task
def mblistmap():
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbmps = mbglobals['__mbmaps__']
    keys_history = sorted([key for key in mbmps.keys() if type(key) == int])
    keys_pin = sorted([key for key in mbmps.keys() if type(key) == str])
    textcases = lambda N: '{0} {1}'.format(N, ['map is', 'maps are'][N>1])

    # list scan(s) in history
    logger.post('{0} stored as history:'.format(textcases(len(keys_history))))
    logger.post('')
    for key in keys_history:
        hd = mbmps[key]['data'].header
        logger.post('label: {0} {1}'.format(key, '(latest)'*(key==0)))
        logger.post('- shape: {0} grid x {1} grid'.format(hd['NAXIS1'], hd['NAXIS2']))
        logger.post('- origin: {0}'.format(hd['ORIGIN']))
        logger.post('- taskflow: {0}'.format(hd['TASKFLOW']))
        logger.post('')

    # list pinned scan(s)
    logger.post('{0} pinned:'.format(textcases(len(keys_pin))))
    logger.post('')
    for key in keys_pin:
        hd = mbmps[key]['data'].header
        logger.post("label: '{0}'".format(key))
        logger.post('- shape: {0} grid x {1} grid'.format(hd['NAXIS1'], hd['NAXIS2']))
        logger.post('- origin: {0}'.format(hd['ORIGIN']))
        logger.post('- taskflow: {0}'.format(hd['TASKFLOW']))
        logger.post('')
