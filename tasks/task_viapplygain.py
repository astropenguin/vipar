# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog
import numpy as np

def viapplygain(mode=None, method=None, gainlist=None, operation=None):
    casalog.origin('viapplygain')
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

    if mode == 'self':
        try:
            l_ga = getattr(np, method)(s_cur, axis=0)
            operator = '/'
            casalog.post('mode: self gain')
        except:
            casalog.post('spam!', 'SEVERE')
            sys.exit()

    elif mode == 'list':
        try:
            l_ga = np.array(gainlist)
            assert len(gainlist) == s_cur.shape[1]
            casalog.post('mode: list gain')
        except:
            casalog.post('spam!', 'SEVERE')
            sys.exit()

        if operation == 'devide':
            operator = '/'
        elif operation == 'multiply':
            operator = '*'
        else:
            casalog.post('spam!', 'SEVERE')
            sys.exit()

    else:
        casalog.post('spam!', 'SEVERE')
        sys.exit()

    s_aga = eval('s_cur {} l_ga'.format(operator))
    casaglobals['__vipar_currentarray__'] = s_aga
    casaglobals['__vipar_previousarray__'] = s_cur
