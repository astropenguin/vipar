# coding: utf-8

# common preamble
import os
import sys
import inspect
import numpy as np
root = os.path.dirname(__file__)
sys.path.append('{}/../'.format(root))
try:
    from taskinit import casalog as logger
except ImportError:
    from viparc.log import pythonlog as logger

# unique preamble
import pyfits as fits
from viparc.stat import Gaussian2D

# definition of task
def mbfitmap(method='Gaussian2D', label=''):
    taskname = sys._getframe().f_code.co_name
    mbglobals = sys._getframe(len(inspect.stack())-1).f_globals
    logger.origin(taskname)

    mbmp = mbglobals['__mbmaps__'][label]

    logger.post('pixel {}'.format(mbmp['data'].header['PIXEL']))
    mp_data = mbmp['data'].data
    mg_daz, mg_del = mbmp.getmeshgrid()

    if method == 'Gaussian2D':
        fitter = Gaussian2D()

    hd_fit, mp_fit = fitter.fit(mg_daz, mg_del, mp_data)

    for i in range(len(hd_fit)):
        try:
            logger.post('{:<8} {:+.5f} / {}'.format(*hd_fit.cards[i]))
        except:
            logger.post('{:<8} {} / {}'.format(*hd_fit.cards[i]))

    hdu_fit = fits.PrimaryHDU(mp_fit, mbmp['data'].header)
    hdu_fit.header['EXTNAME'] = 'FIT'
    hdu_fit.header += hd_fit

    mbmp.append(hdu_fit)
    mbmp.recordtask(taskname)
    mbglobals['__mbmaps__'].append(mbmp)

    return dict(hdu_fit.header)
