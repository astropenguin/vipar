# coding: utf-8

import numpy as np

def makegrid(az_or_el, gridsize):
    gridnum = np.floor(np.ptp(az_or_el) / gridsize) + 1
    gridstart = np.ceil(np.min(az_or_el / gridsize)) * gridsize
    grid = np.arange(gridstart, gridstart+gridsize*gridnum, gridsize)
    return grid

def rectanglemap(ts_pixel, ts_az, ts_el, gridsize_az, gridsize_el):
    grid_az = makegrid(ts_az, gridsize_az)
    grid_el = makegrid(ts_el, gridsize_el)
    tile_az = np.tile(grid_az, (len(ts_pixel), 1))
    tile_el = np.tile(grid_el, (len(ts_pixel), 1))
    ts_indices_az = np.argmin(np.abs(tile_az.T - ts_az), axis=0)
    ts_indices_el = np.argmin(np.abs(tile_el.T - ts_el), axis=0)

    mp_input = np.zeros([len(grid_az), len(grid_el)])
    mp_count = np.zeros([len(grid_az), len(grid_el)])

    for t in range(len(ts_pixel)):
        i, j = ts_indices_el[t], ts_indices_az[t]
        mp_input[i,j] += ts_pixel[t]
        mp_count[i,j] += 1.0

    mp_az, mp_el = np.meshgrid(grid_az, grid_el)
    mp_value = mp_input / np.ma.array(mp_count, mask=(mp_count==0.0))
    mp_output = np.array([mp_az, mp_el, mp_value])

    return mp_output
