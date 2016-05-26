# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog
import numpy as np

cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/../'.format(cwd))
from viparc.statistics import PCA

def viremovenoise(method=None, pixellist=None, fraction=None):
    casalog.origin('viremovenoise')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    try:
        f = casaglobals['__vipar_mbfits__']
    except KeyError:
        casalog.post('MBFITS is not opened', 'SEVERE')

    try:
        s_cur = casaglobals['__vipar_currentarray__']
    except KeyError:
        casalog.post('current array is not stored', 'SEVERE')

    if len(pixellist) == 0:
        try:
            mask = np.zeros_like(s_cur, dtype=bool)
            s_ma = np.ma.array(s_cur, mask=mask)
        except :
            casalog.post('spam!', 'SEVERE')

    else:
        try:
            mask = np.ones_like(s_cur, dtype=bool)
            for pixel in pixellist:
                ma[:pixel-1] = False
            s_ma = np.ma.array(s_cur, mask=mask)
        except :
            casalog.post('spam!', 'SEVERE')

    if method == 'pca':
        try:
            pca = PCA(s_ma)
            assert 0.0 < fraction < 1.0
            s_noi = pca.reconstruct(fraction)
        except:
            casalog.post('spam!', 'SEVERE')

    elif method in ['median', 'mean']:
        try:
            t_noi = getattr(np, method)(s_ma, axis=1)
            s_noi = np.tile(t_noi, (s_cur.shape[1],1)).T
        except:
            casalog.post('spam!', 'SEVERE')

    s_rmn = s_cur - s_noi
    casaglobals['__vipar_currentarray__'] = s_rmn
    casaglobals['__vipar_previousarray__'] = s_cur
