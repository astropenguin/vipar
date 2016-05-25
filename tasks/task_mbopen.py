# coding: utf-8

import os
import sys
import inspect
from taskinit import *
from astropy.io import fits

def mbopen(mbfits=None, mode=None, memmap=None):
    casalog.origin('mbopen')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals
    try:
        casaglobals['_mbfits'] = fits.open(mbfits, mode, memmap)
        casalog.post('a MBFITS successfully open as _mbfits')
    except:
        casalog.post('name of MBFITS is not spacified', 'SEVERE')
