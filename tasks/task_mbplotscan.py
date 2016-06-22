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

# definition of task
def mbplotscan(pixellist=[1,2], label=''):
    depth = [s[3] for s in inspect.stack()].index('<module>')
    mbglobals = sys._getframe(depth).f_globals
    taskname = sys._getframe().f_code.co_name
    logger.origin(taskname)

    mbsc = mbglobals['__mbscans__'][label]
    mjd = mbsc['record'].data['MJD']

    ax = plt.gca()
    for pixel in pixellist:
        ts = mbsc['data'].data[:,pixel-1]
        ax.plot(mjd, ts, label='Pixel No. {0}'.format(pixel))

    ax.set_xlim([mjd.min(), mjd.max()])
    ax.set_xlabel('MJD (day)')
    ax.legend()
