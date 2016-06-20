# coding: utf-8

'''
map.py - Vipar's scan-to-map converter module

+ developer: Akio Taniguchi (IoA, UTokyo)
+ contact: taniguchi@ioa.s.u-tokyo.ac.jp
'''

# common preamble
import os
import sys
import inspect
import numpy as np

# unique preamble
import pyfits as fits


class SinglePixel(object):
    def __init__(self, pixel, gridsize, gridrefval=[0.0,0.0]):
        self.pixel = pixel
        self.gridsize = gridsize
        self.gridrefval = gridrefval

    def __call__(self, mbsc):
        ts_pixel = mbsc['data'].data[:,self.pixel-1]
        ts_daz = mbsc['record'].data['dAz'] * 3600.0 # arcsec
        ts_del = mbsc['record'].data['dEl'] * 3600.0 # arcsec

        # make map
        grid_daz = self._makegrid(ts_daz, self.gridsize[0], self.gridrefval[0])
        grid_del = self._makegrid(ts_del, self.gridsize[1], self.gridrefval[1])
        mp = self._makemap(ts_pixel, ts_daz, ts_del, grid_daz, grid_del)

        # make header
        header = fits.Header()
        header['METHOD'] = 'single'
        header['PIXEL'] = self.pixel
        header['ORIGIN'] = mbsc['data'].header['ORIGIN']
        header['CRPIX1'] = np.argmin(np.abs(grid_daz-self.gridrefval[0])) + 1
        header['CRPIX2'] = np.argmin(np.abs(grid_del-self.gridrefval[1])) + 1
        header['CDELT1'], header['CDELT2'] = self.gridsize
        header['CRVAL1'], header['CRVAL2'] = self.gridrefval
        header['CTYPE1'] = header['CTYPE2'] = 'LINEAR'
        header['CUNIT1'] = header['CUNIT2'] = 'deg'

        return mp, header

    def _makegrid(self, ts_d__, gridsize, gridrefval=0.0):
        ts = ts_d__ - gridrefval

        # grid of left side
        gridl_range = (np.floor(np.min(ts/gridsize)) * gridsize, 0.0)
        gridl = np.arange(gridl_range[0], gridl_range[1], gridsize)

        # grid of right side
        gridr_range = (0.0, np.ceil(np.max(ts/gridsize)) * gridsize)
        gridr = np.arange(gridr_range[0], gridr_range[1]+gridsize, gridsize)

        # grid of both side
        grid = np.hstack([gridl, gridr]) + gridrefval
        return grid

    def _makemap(self, ts_pixel, ts_daz, ts_del, grid_daz, grid_del):
        # preprocessing
        tile_daz = np.tile(grid_daz, (len(ts_pixel), 1))
        tile_del = np.tile(grid_del, (len(ts_pixel), 1))

        # timestream indices of dAz, dEl
        ts_idaz = np.argmin(np.abs(tile_daz.T - ts_daz), axis=0)
        ts_idel = np.argmin(np.abs(tile_del.T - ts_del), axis=0)

        mp_input = np.zeros([len(grid_del), len(grid_daz)])
        mp_count = np.zeros([len(grid_del), len(grid_daz)])

        for t in range(len(ts_pixel)):
            mp_input[ts_idel[t],ts_idaz[t]] += ts_pixel[t]
            mp_count[ts_idel[t],ts_idaz[t]] += 1.0

        mp_data = mp_input / mp_count
        return mp_data


class MultiPixels(object):
    def __init__(self, rcp, gridsize, gridrefval=[0.0,0.0]):
        self.rcp = rcp
        self.gridsize = gridsize
        self.gridrefval = gridrefval

    def __call__(self, mbsc):
        pass

    def _makegrid(self):
        pass

    def _makemap(self):
        pass
