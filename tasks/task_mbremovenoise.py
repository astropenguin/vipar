# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog
import numpy as np

# import viparc libraries
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/../'.format(cwd))
from viparc.statistics import PCA

def mbremovenoise(method=None, pixellist=None, fraction=None):
    casalog.origin('mbremovenoise')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    sc_pre = casaglobals['__vipar_currentscan__']

    if not pixellist == []:
        sc_mask = np.ones_like(sc_pre, dtype=bool)
        for pixel in pixellist:
            sc_mask[:,pixel-1] = False
        sc_pre = np.ma.array(sc_pre, mask=sc_mask)

    if method == 'pca':
        pca = PCA(sc_pre)
        sc_noi = pca.reconstruct(fraction)

    elif method in ['median', 'mean']:
        ts_noi = getattr(np, method)(sc_pre, axis=1)
        sc_noi = np.tile(ts_noi, (sc_pre.shape[1],1)).T

    sc_cur = sc_pre - sc_noi

    casaglobals['__vipar_currentscan__'] = sc_cur
    casaglobals['__vipar_previousscan__'] = sc_pre
