# coding: utf-8

import os
import sys
import inspect
from datetime import datetime
from taskinit import casalog

def mbundoscan(label=None):
    casalog.origin('mbundoscan')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    if label == '':
        sc_pre = casaglobals['__vipar_previousscan__']
        casaglobals['__vipar_currentscan__'] = sc_pre
        casaglobals.pop('__vipar_previousscan__')
    else:
        sc_rec = casaglobals['__vipar_recorededscans__'][label]
        casaglobals['__vipar_currentscan__'] = sc_rec
        casaglobals.pop('__vipar_previousscan__')
