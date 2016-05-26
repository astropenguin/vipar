# coding: utf-8

import os
import sys
import inspect
from datetime import datetime
from taskinit import casalog

def mbundomap(label=None):
    casalog.origin('mbundomap')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    if label == '':
        mp_pre = casaglobals['__vipar_previousmap__']
        casaglobals['__vipar_currentmap__'] = mp_pre
        casaglobals.pop('__vipar_previousmap__')
    else:
        mp_rec = casaglobals['__vipar_recorededmaps__'][label]
        casaglobals['__vipar_currentmap__'] = mp_rec
        casaglobals.pop('__vipar_previousmap__')
