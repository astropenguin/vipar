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
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# definition of task
def mbplotmap(raster='data', contour='fit', label=''):
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbmp = mbglobals['__mbmaps__'][label]
    mg_daz, mg_del = mbmp.getmeshgrid()

    ax = plt.gca()
    ax.set_xlim([np.min(mg_daz), np.max(mg_daz)])
    ax.set_ylim([np.min(mg_del), np.max(mg_del)])
    ax.set_xlabel('dAz (arcsec)')
    ax.set_ylabel('dEl (arcsec)')

    # raster map
    mp = mbmp[raster].data
    mp_raster = np.ma.array(mp, mask=np.isnan(mp))
    ax.pcolormesh(mg_daz, mg_del, mp_raster, cmap='inferno')

    # contour map (optional)
    try:
        mp_contour = mbmp[contour].data
        ax.contour(mg_daz, mg_del, mp_contour)
    except:
        logger.post('fit map is not contained', 'WARN')
