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
def mbsubtractbaseline(method='median', label=''):
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbsc = mbglobals['__mbscans__'][label]
    sc_old = mbsc['data'].data

    logger.post('method: {0}'.format(method))
    try:
        fr_baseline = getattr(np, method)(sc_old, axis=0)
        sc_new = sc_old - fr_baseline
        logger.post('baseline is successfully estimated')
    except:
        logger.post('an error occured', 'ERROR')

    mbsc['data'].data = sc_new
    mbsc.recordtask(taskname)
    mbglobals['__mbscans__'].append(mbsc)

    logger.post('baseline is successfully subtracted from MBScan')
    logger.post('new MBScan is now stored as __mbscans__[0]')
