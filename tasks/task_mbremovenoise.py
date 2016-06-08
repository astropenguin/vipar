# coding: utf-8

import os
import sys
import inspect
from copy import deepcopy
from taskinit import casalog
import numpy as np

# import viparc libraries
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/../'.format(cwd))
from viparc.statistics import PCA

def mbremovenoise(method=None, pixellist=None, fraction=None):
    casalog.origin('mbremovenoise')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    sc_previous = deepcopy(casaglobals['__vipar_scans__'][0])

    if pixellist == []:
        sc_target = sc_previous
    else:
        sc_target = sc_previous[:,np.array(pixellist)-1]

    if method == 'pca':
        fr_gain = np.ptp(sc_target, axis=0) # effective gain
        pca = PCA(sc_target / fr_gain)
        sc_noise = pca.reconstruct(fraction) * fr_gain

    elif method in ['median', 'mean']:
        ts_noise = getattr(np, method)(sc_target, axis=1)
        sc_noise = np.tile(ts_noise, (sc_target.shape[1],1)).T

    if pixellist == []:
        sc_current = sc_target - sc_noise
    else:
        sc_current = np.zeros_like(sc_previous)
        sc_current[:,np.array(pixellist)-1] = sc_target - sc_noise

    casaglobals['__vipar_scans__'].append(sc_current)
