# coding: utf-8

import os
import sys
import inspect
from itertools import product
from taskinit import casalog
import numpy as np
import matplotlib.pyplot as plt

try:
    import pyfits as fits
except ImportError:
    from astropy.io import fits

try:
    import seaborn as sns
    sns.set_context('talk')
except:
    casalog.post('seaborn is not installed', 'WARN')

# import viparc libraries
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/../'.format(cwd))
from viparc.database import ViparDB
from viparc.mapping import rectanglemap

def mbmakepixelmap(pixel=None, gridsize=None, show=None, save=None):
    casalog.origin('mbmakepixelmap')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    f = casaglobals['__vipar_mbfits__']
    ts_pixel = casaglobals['__vipar_scans__'][0][:,pixel-1]
    ts_az = f['datapar-mbfits'].data['longoff'] * 3600.0 # arcsec
    ts_el = f['datapar-mbfits'].data['latoff'] * 3600.0 # arcsec
    gridsize_az = gridsize[0] if type(gridsize) == list else gridsize
    gridsize_el = gridsize[1] if type(gridsize) == list else gridsize

    mp_current = rectanglemap(ts_pixel, ts_az, ts_el, gridsize_az, gridsize_el)

    if not '__vipar_maps__' in casaglobals.keys():
        casaglobals['__vipar_maps__'] = ViparDB()

    casaglobals['__vipar_maps__'].append(mp_current)

    if save:
        mp_az, mp_el, mp_value = mp_current
        hdu = fits.PrimaryHDU(mp_value)
        hdu.header['bscale'] = 1.0
        hdu.header['bzero'] = 0.0
        hdu.header['ctype1'] = 'AZ'
        hdu.header['crpix1'] = 1.0
        hdu.header['crval1'] = mp_az.min() / 3600.0
        hdu.header['crdelt1'] = gridsize_az / 3600.0
        hdu.header['crunit1'] = 'deg'
        hdu.header['ctype2'] = 'EL'
        hdu.header['crpix2'] = 1.0
        hdu.header['crval2'] = mp_el.min() / 3600.0
        hdu.header['crdelt2'] = gridsize_el / 3600.0
        hdu.header['crunit2'] = 'deg'
        basename = f.filename().rstrip('fits.gz').rstrip('fits')
        hdu.writeto('{}.pixelmap.{}.fits'.format(basename, pixel))

    if show:
        fig = plt.figure(figsize=(8,6))
        ax0 = fig.add_subplot(111)
        ax0.set_aspect('equal')
        mp_az, mp_el, mp_value = mp_current
        try:
            cmap = sns.cubehelix_palette(8, as_cmap=True)
            cax = ax0.pcolormesh(mp_az, mp_el, mp_value, cmap=cmap)
        except:
            cax = ax0.pcolormesh(mp_az, mp_el, mp_value)

        ax0.set_xlim([mp_az.min(), mp_az.max()])
        ax0.set_ylim([mp_el.min(), mp_el.max()])
        ax0.set_xlabel('Longitude Offset (arcsec)')
        ax0.set_ylabel('Latitude Offset (arcsec)')
        ax0.set_title('Pixel No.{}'.format(pixel))
        fig.colorbar(cax)
        plt.show()
