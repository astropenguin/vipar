# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog
import numpy as np

def viapplybaseline(method=None):
    casalog.origin('viapplybaseline')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    try:
        f = casaglobals['__vipar_mbfits__']
    except KeyError:
        casalog.post('MBFITS is not opened', 'SEVERE')
        sys.exit()

    try:
        s_cur = casaglobals['__vipar_currentarray__']
    except KeyError:
        casalog.post('current array is not stored', 'SEVERE')
        sys.exit()

    try:
        s_bl = getattr(np, method)(s_cur, axis=0)
    except AttributeError:
        casalog.post('invalid method: {}'.format(mode), 'SEVERE')
        sys.exit()

    s_abl = s_cur - s_bl
    casaglobals['__vipar_currentarray__'] = s_abl
    casaglobals['__vipar_previousarray__'] = s_cur
