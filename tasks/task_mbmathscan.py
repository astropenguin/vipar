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
def mbmathscan(expression='SC0+SC1', label0='', label1=''):
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbsc_0 = mbglobals['__mbscans__'][0 if label0=='' else label0]
    mbsc_1 = mbglobals['__mbscans__'][1 if label1=='' else label1]
    sc_0 = mbsc_0['data'].data
    sc_1 = mbsc_1['data'].data

    # place holder
    expression = expression.lower()
    phlist_0 = ['l0', 'label0', 's0', 'sc0', 'scan0']
    phlist_1 = ['l1', 'label1', 's1', 'sc1', 'scan1']
    ph_0 = [ph for ph in phlist_0 if ph in expression][0]
    expression = expression.replace(ph_0, 'sc_0')
    try:
        ph_1 = [ph for ph in phlist_1 if ph in expression][0]
        expression = expression.replace(ph_1, 'sc_1')
    except:
        logger.post('second scan is not spacified', 'WARN')

    # calculation
    try:
        sc_new = eval(expression)
    except:
        logger.post('an error occured', 'ERROR')

    mbsc_0['data'].data = sc_new
    mbsc_0.recordtask(taskname)
    mbglobals['__mbscans__'].append(mbsc_0)

    logger.post('calculation is successfully finished')
    logger.post('new MBScan is now stored as __mbscans__[0]')
