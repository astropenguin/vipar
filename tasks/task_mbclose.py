# coding: utf-8

import os
import sys
import inspect
from taskinit import *

def mbclose():
    casalog.origin('mbclose')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals
    try:
        casaglobals['_mbfits'].close()
        casalog.post('open MBFITS successfully closed')
    except:
        casalog.post('open MBFITS does not exist', 'SEVERE')
