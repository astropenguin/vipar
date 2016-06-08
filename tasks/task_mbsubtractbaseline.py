# coding: utf-8

import os
import sys
import inspect
from copy import deepcopy
from taskinit import casalog
import numpy as np

def mbsubtractbaseline(method=None):
    casalog.origin('mbsubtractbaseline')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    sc_previous = deepcopy(casaglobals['__vipar_scans__'][0])

    fr_baseline = getattr(np, method)(sc_previous, axis=0)
    sc_current = sc_previous - fr_baseline

    casaglobals['__vipar_scans__'].append(sc_current)
