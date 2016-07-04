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
import json
import pyfits as fits
from collections import OrderedDict


class DefaultConverter(object):
    def __init__(self, rcpfile, pixels=[], gain='point', gridsizes=[6.0,6.0], gridrefvals=[0.0,0.0]):
        self.gridsizes = gridsizes
        self.gridrefvals = gridrefvals
        self.hdu_rcp = self._parsercp(rcpfile)
        self.pixels = np.array(pixels) if pixels != [] else self._selectpixels(gain)

    def __call__(self, mbsc):
        sc = mbsc['DATA'].data
        ts_daz = mbsc['RECORD'].data['DAZ']
        ts_del = mbsc['RECORD'].data['DEL']

        # make map
        grid_daz = self._makegrid(ts_daz, 'DAZ', self.gridsizes[0], self.gridrefvals[0])
        grid_del = self._makegrid(ts_del, 'DEL', self.gridsizes[1], self.gridrefvals[1])
        mp_data = self._makemap(sc, ts_daz, ts_del, grid_daz, grid_del)

        # HDUs
        hdu_data = fits.PrimaryHDU(mp_data)
        hdu_data.header['EXTNAME'] = 'DATA'
        hdu_data.header['METHOD'] = 'default'
        hdu_data.header['PIXELS'] = ','.join([str(pixel) for pixel in self.pixels])
        hdu_data.header['ORIGIN'] = mbsc['DATA'].header['ORIGIN']
        hdu_data.header['CRPIX1'] = np.argmin(np.abs(grid_daz-self.gridrefvals[0])) + 1
        hdu_data.header['CRPIX2'] = np.argmin(np.abs(grid_del-self.gridrefvals[1])) + 1
        hdu_data.header['CDELT1'], hdu_data.header['CDELT2'] = self.gridsizes
        hdu_data.header['CRVAL1'], hdu_data.header['CRVAL2'] = self.gridrefvals
        hdu_data.header['CTYPE1'] = hdu_data.header['CTYPE2'] = 'LINEAR'
        hdu_data.header['CUNIT1'] = hdu_data.header['CUNIT2'] = 'deg'

        hdu_record = mbsc['RECORD']
        hdu_rcp = self.hdu_rcp

        return hdu_data, hdu_record, hdu_rcp

    def _makemap(self, sc, ts_daz, ts_del, grid_daz, grid_del):
        # map arrays for all pixels
        mp_inputsum = np.zeros([len(grid_del), len(grid_daz)])
        mp_weightsum = np.zeros([len(grid_del), len(grid_daz)])

        # preprocessing
        tile_daz = np.tile(grid_daz, (len(sc), 1)).T
        tile_del = np.tile(grid_del, (len(sc), 1)).T

        # map of each pixel
        for pixel in self.pixels:
            print('pixel: {0}'.format(pixel))
            # map arrays for each pixel
            mp_input = np.zeros([len(grid_del), len(grid_daz)])
            mp_count = np.zeros([len(grid_del), len(grid_daz)])

            # timestream indices of dAz, dEl
            ts_mdaz = ts_daz - self.hdu_rcp.data['DAZ'][pixel-1]
            ts_mdel = ts_del - self.hdu_rcp.data['DEL'][pixel-1]
            ts_idaz = np.argmin(np.abs(tile_daz - ts_mdaz), axis=0)
            ts_idel = np.argmin(np.abs(tile_del - ts_mdel), axis=0)

            for t in range(len(sc)):
                mp_input[ts_idel[t],ts_idaz[t]] += sc[t,pixel-1]
                mp_count[ts_idel[t],ts_idaz[t]] += 1.0

            # weight map
            mp_count[mp_count==0.0] = np.nan
            mp_mean = mp_input / mp_count
            mp_weight = self._sd(mp_mean, mp_count)**-2

            # add
            mp_inputsum += np.nan_to_num(mp_weight*mp_input)
            mp_weightsum += np.nan_to_num(mp_weight*mp_count)

        # weighted map
        mp_weightsum[mp_weightsum==0.0] = np.nan
        mp_data = mp_inputsum / mp_weightsum

        return mp_data

    def _selectpixels(self, gain):
        if gain == 'point':
            pixels_gain = self.hdu_rcp.data['GAIN_PNT'] != 0.0
        elif gain == 'extended':
            pixels_gain = self.hdu_rcp.data['GAIN_EXT'] != 0.0

        pixels_daz = ~np.isnan(self.hdu_rcp.data['dAz'])
        pixels_del = ~np.isnan(self.hdu_rcp.data['dEl'])

        mask = pixels_gain & pixels_daz & pixels_del

        return self.hdu_rcp.data['PIXEL'][mask]

    def _makegrid(self, ts_d__, coord='DAZ', gridsize=6.0, gridrefval=0.0):
        # preprocessing
        ts = ts_d__ - gridrefval

        # grid of left side
        coord_min = np.min(ts) - np.nanmax(self.hdu_rcp.data[coord][self.pixels-1])
        gridl_range = (np.floor(coord_min/gridsize) * gridsize, 0.0)
        gridl = np.arange(gridl_range[0], gridl_range[1], gridsize)

        # grid of right side
        coord_max = np.max(ts) - np.nanmin(self.hdu_rcp.data[coord][self.pixels-1])
        gridr_range = (0.0, np.ceil(coord_max/gridsize) * gridsize)
        gridr = np.arange(gridr_range[0], gridr_range[1]+gridsize, gridsize)

        # grid of both side
        grid = np.hstack([gridl, gridr]) + gridrefval

        return grid

    @staticmethod
    def _parsercp(rcpfile):
        with open(rcpfile) as f:
            d = json.load(f, object_pairs_hook=OrderedDict)

        pixel = np.array(d.keys(), int)
        g_pnt = np.array([d[key]['Gain_point'] for key in d], float)
        g_ext = np.array([d[key]['Gain_extended'] for key in d], float)
        p_daz = -np.array([d[key]['dAz'] for key in d], float)
        p_del = -np.array([d[key]['dEl'] for key in d], float)

        alist = [pixel, p_daz, p_del, g_pnt, g_ext]
        names = ['PIXEL', 'DAZ', 'DEL', 'GAIN_PNT', 'GAIN_EXT']
        dtypes = ['i8', 'f8', 'f8', 'f8', 'f8']
        rcp = np.rec.fromarrays(alist, zip(names, dtypes))

        hdu_rcp = fits.BinTableHDU(rcp)
        hdu_rcp.header['EXTNAME'] = 'RCP'
        hdu_rcp.header['ORIGIN'] = os.path.basename(rcpfile)

        return hdu_rcp

    @staticmethod
    def _sd(array, weight):
        '''Calculate S.D. of an array with jackknife method.

        Args:
        - array (array): array of input data
        - weight (array): array of weight corresponding data

        Returns:
        - sd_jk (float): S.D. of a map
        '''
        a = array[~np.isnan(array)]
        w = weight[~np.isnan(weight)]
        N = a.size

        a_jk = (np.sum(w*a) - w*a) / (np.sum(w)-w)
        sd_jk = (N-1) * np.std(a_jk)

        return sd_jk


class PointingConverter(object):
    def __init__(self, pixel, gridsizes=[6.0,6.0], gridrefvals=[0.0,0.0]):
        self.pixel = pixel
        self.gridsizes = gridsizes
        self.gridrefvals = gridrefvals

    def __call__(self, mbsc):
        ts_pixel = mbsc['DATA'].data[:,self.pixel-1]
        ts_daz = mbsc['RECORD'].data['DAZ']
        ts_del = mbsc['RECORD'].data['DEL']

        # make map
        grid_daz = self._makegrid(ts_daz, self.gridsizes[0], self.gridrefvals[0])
        grid_del = self._makegrid(ts_del, self.gridsizes[1], self.gridrefvals[1])
        mp_data = self._makemap(ts_pixel, ts_daz, ts_del, grid_daz, grid_del)

        # HDUs
        hdu_data = fits.PrimaryHDU(mp_data)
        hdu_data.header['EXTNAME'] = 'DATA'
        hdu_data.header['METHOD'] = 'pointing'
        hdu_data.header['PIXEL'] = self.pixel
        hdu_data.header['ORIGIN'] = mbsc['DATA'].header['ORIGIN']
        hdu_data.header['CRPIX1'] = np.argmin(np.abs(grid_daz-self.gridrefvals[0])) + 1
        hdu_data.header['CRPIX2'] = np.argmin(np.abs(grid_del-self.gridrefvals[1])) + 1
        hdu_data.header['CDELT1'], hdu_data.header['CDELT2'] = self.gridsizes
        hdu_data.header['CRVAL1'], hdu_data.header['CRVAL2'] = self.gridrefvals
        hdu_data.header['CTYPE1'] = hdu_data.header['CTYPE2'] = 'LINEAR'
        hdu_data.header['CUNIT1'] = hdu_data.header['CUNIT2'] = 'deg'

        hdu_record = mbsc['RECORD']

        return hdu_data, hdu_record

    @staticmethod
    def _makegrid(ts_d__, gridsize=6.0, gridrefval=0.0):
        # preprocessing
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

    @staticmethod
    def _makemap(ts_pixel, ts_daz, ts_del, grid_daz, grid_del):
        # preprocessing
        tile_daz = np.tile(grid_daz, (len(ts_pixel), 1))
        tile_del = np.tile(grid_del, (len(ts_pixel), 1))

        # map arrays
        mp_input = np.zeros([len(grid_del), len(grid_daz)])
        mp_count = np.zeros([len(grid_del), len(grid_daz)])

        # timestream indices of dAz, dEl
        ts_i_daz = np.argmin(np.abs(tile_daz.T - ts_daz), axis=0)
        ts_i_del = np.argmin(np.abs(tile_del.T - ts_del), axis=0)

        for t in range(len(ts_pixel)):
            mp_input[ts_i_del[t],ts_i_daz[t]] += ts_pixel[t]
            mp_count[ts_i_del[t],ts_i_daz[t]] += 1.0

        mp_count[mp_count==0.0] = np.nan
        mp_data = mp_input / mp_count

        return mp_data
