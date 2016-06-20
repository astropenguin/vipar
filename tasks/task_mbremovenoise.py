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
from viparc.stat import PCA

# definition of task
def mbremovenoise(method='PCA', pixellist=[], label='', fraction=0.9):
    taskname = sys._getframe().f_code.co_name
    mbglobals = sys._getframe(len(inspect.stack())-1).f_globals
    logger.origin(taskname)

    mbsc = mbglobals['__mbscans__'][label]
    sc_old = mbsc['data'].data

    if pixellist == []:
        logger.post('pixels used for estimation: all')
        sc_target = sc_old
    else:
        logger.post('pixels used for estimation: {}'.format(pixellist))
        sc_target = sc_old[:,np.array(pixellist)-1]

    logger.post('method: {}'.format(method))
    try:
        if method == 'PCA':
            fr_gain = np.ptp(sc_target, axis=0) # effective gain
            pca = PCA(sc_target / fr_gain)
            sc_noise = pca.reconstruct(fraction) * fr_gain

        elif method in ['median', 'mean']:
            ts_noise = getattr(np, method)(sc_target, axis=1)
            sc_noise = np.tile(ts_noise, (sc_target.shape[1], 1)).T

        logger.post('correlated noise is successfully estimated')
    except:
        logger.post('an error occured', 'ERROR')

    if pixellist == []:
        sc_new = sc_target - sc_noise
    else:
        sc_new = np.zeros_like(sc_old)
        sc_new[:,np.array(pixellist)-1] = sc_target - sc_noise

    mbsc['data'].data = sc_new
    mbsc.recordtask(taskname)
    mbglobals['__mbscans__'].append(mbsc)

    logger.post('correlated noise is successfully subtracted from MBScan')
    logger.post('new MBScan is now stored as __mbscans__[0]')
