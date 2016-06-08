# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog

def mbundomap(label=None):
    casalog.origin('mbundomap')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    casaglobals['__vipar_maps__'].undo(label)
