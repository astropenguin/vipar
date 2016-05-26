# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog

def mbclose():
    casalog.origin('mbclose')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    casaglobals['__vipar_mbfits__'].close()
