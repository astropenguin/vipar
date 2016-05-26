# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog

def viclose():
    casalog.origin('viclose')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals
    try:
        casaglobals['__vipar_mbfits__'].close()
        casalog.post('opening MBFITS successfully closed')

    except:
        casalog.post('opening MBFITS does not exist', 'SEVERE')
