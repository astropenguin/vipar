# coding: utf-8

# common preamble
import os
import sys
import inspect
import numpy as np
root = os.path.dirname(__file__)
sys.path.append('{0}/../'.format(root))
incasa = '__CASAPY_PYTHONDIR' in os.environ
if incasa:
    from taskinit import casalog as logger
else:
    from viparc.log import pythonlog as logger

# unique preamble
import pyfits as fits
from viparc.stat import Gaussian2D

# definition of task
def mbfitmap(method='Gaussian2D', label=''):
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbmp = mbglobals['__mbmaps__'][label]

    mp_data = mbmp['data'].data
    mg_daz, mg_del = mbmp.getmeshgrid()

    if method == 'Gaussian2D':
        fitter = Gaussian2D()

    hd_fit, mp_fit = fitter(mg_daz, mg_del, mp_data)

    for i in range(len(hd_fit)):
        try:
            logger.post('{0:<8} {1:+.5f} / {2}'.format(*hd_fit.cards[i]))
        except:
            logger.post('{0:<8} {1} / {2}'.format(*hd_fit.cards[i]))

    hdu_fit = fits.PrimaryHDU(mp_fit, mbmp['data'].header)
    hdu_fit.header['EXTNAME'] = 'FIT'
    hdu_fit.header += hd_fit

    mbmp.append(hdu_fit)
    mbmp.recordtask(taskname)
    mbglobals['__mbmaps__'].append(mbmp)

    return dict(hdu_fit.header)
