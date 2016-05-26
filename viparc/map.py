# coding: utf-8

import numpy as np
import scipy.special as sp

def grid(lon_or_lat, gridsize):
    gridnum = np.floor(np.ptp(lon_or_lat) / gridsize) + 1
    gridstart = np.ceil(np.min(lon_or_lat / gridsize)) * gridsize
    grid = np.arange(gridstart, gridstart+gridsize*gridnum, gridsize)
    return grid
