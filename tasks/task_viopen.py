# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog
import numpy as np
from astropy.io import fits

def viopen(mbfits=None, mode=None, memmap=None):
    casalog.origin('viopen')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    try:
        f = fits.open(mbfits, mode, memmap)
        s_cur = np.array(f['arraydata-mbfits'].data.DATA[:,:,0])
    except IOError:
        casalog.post('MBFITS does not exist', 'SEVERE')
    except TypeError:
        casalog.post('name of MBFITS is not spacified', 'SEVERE')

    casaglobals['__vipar_mbfits__'] = f
    casaglobals['__vipar_currentarray__'] = s_cur
    casalog.post('MBFITS is successfully opened')
    casalog.post('current array data is stored as __vipar_currentarray__')
