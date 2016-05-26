# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog
import numpy as np

def mbapplybaseline(method=None):
    casalog.origin('mbapplybaseline')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    sc_pre = casaglobals['__vipar_currentscan__']

    sc_bln = getattr(np, method)(sc_pre, axis=0)
    sc_cur = sc_pre - sc_bln

    casaglobals['__vipar_currentscan__'] = sc_cur
    casaglobals['__vipar_previousscan__'] = sc_pre
