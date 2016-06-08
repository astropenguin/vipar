# coding: utf-8

import os
import sys
import inspect
from datetime import datetime
from taskinit import casalog

def mbundoscan(label=None):
    casalog.origin('mbundoscan')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals


    casaglobals['__vipar_scans__'].undo(label)
