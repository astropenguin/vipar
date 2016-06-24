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
def mbmathmap(expression='MP0+MP1', label0='', label1=''):
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbmp_0 = mbglobals['__mbmaps__'][0 if label0=='' else label0]
    mbmp_1 = mbglobals['__mbmaps__'][1 if label1=='' else label1]
    mp_0 = mbmp_0['data'].data
    mp_1 = mbmp_1['data'].data

    # place holder
    expression = expression.lower()
    phlist_0 = ['l0', 'label0', 'm0', 'mp0', 'map0']
    phlist_1 = ['l1', 'label1', 'm1', 'mp1', 'map1']
    ph_0 = [ph for ph in phlist_0 if ph in expression][0]
    expression = expression.replace(ph_0, 'mp_0')
    try:
        ph_1 = [ph for ph in phlist_1 if ph in expression][0]
        expression = expression.replace(ph_1, 'mp_1')
    except:
        logger.post('second map is not spacified', 'WARN')

    # calculation
    try:
        mp_new = eval(expression)
    except:
        logger.post('an error occured', 'ERROR')

    mbmp_0['data'].data = mp_new
    mbmp_0.recordtask(taskname)
    mbglobals['__mbmaps__'].append(mbmp_0)

    logger.post('calculation is successfully finished')
    logger.post('new MBMap is now stored as __mbmaps__[0]')
