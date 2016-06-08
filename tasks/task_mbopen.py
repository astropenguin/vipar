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

# import viparc libraries
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/../'.format(cwd))
from viparc.database import ViparDB

def mbopen(mbfits=None, mode=None, memmap=None):
    casalog.origin('mbopen')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    f = fits.open(mbfits, mode, memmap)
    sc_current = np.squeeze(f['arraydata-mbfits'].data.DATA)

    casaglobals['__vipar_mbfits__'] = f
    casaglobals['__vipar_scans__'] = ViparDB()
    casaglobals['__vipar_scans__'].append(sc_current)
