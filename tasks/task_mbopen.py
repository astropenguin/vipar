# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog
import numpy as np
try:
    import pyfits as fits
except ImportError:
    from astropy.io import fits

def mbopen(mbfits=None, mode=None, memmap=None):
    casalog.origin('mbopen')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    f = fits.open(mbfits, mode, memmap)
    sc_cur = np.squeeze(f['arraydata-mbfits'].data.DATA)

    casaglobals['__vipar_mbfits__'] = f
    casaglobals['__vipar_currentscan__'] = sc_cur
