# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog
import numpy as np

def mbapplygain(mode=None, method=None, gainlist=None, operation=None):
    casalog.origin('mbapplygain')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    sc_pre = casaglobals['__vipar_currentscan__']

    if mode == 'self':
        fr_gain = getattr(np, method)(sc_pre, axis=0)
        operator = '/'

    elif mode == 'list':
        fr_gain = np.array(gainlist)

        if operation == 'devide':
            operator = '/'
        elif operation == 'multiply':
            operator = '*'

    sc_cur = eval('sc_pre {} fr_gain'.format(operator))

    casaglobals['__vipar_currentscan__'] = sc_cur
    casaglobals['__vipar_previousscan__'] = sc_pre
