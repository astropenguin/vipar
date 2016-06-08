# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog

def mbrecordscan(label=None):
    casalog.origin('mbrecordscan')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    casaglobals['__vipar_scans__'].record(label)
