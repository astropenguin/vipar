# coding: utf-8

import os
import sys
import inspect
from itertools import product
from taskinit import casalog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
try:
    import seaborn as sns
    sns.set_context('talk')
except:
    casalog.post('seaborn is not installed', 'WARN')

# import viparc libraries
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/../'.format(cwd))
from viparc.map import grid

def mbmakemapdev(pixel=None, gridsize=None, show=None):
    casalog.origin('mbmakemapdev')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    f = casaglobals['__vipar_mbfits__']
    ts_cur = casaglobals['__vipar_currentscan__'][:,pixel-1]
    ts_lon = f['datapar-mbfits'].data['longoff'] * 3600.0 # arcsec
    ts_lat = f['datapar-mbfits'].data['latoff'] * 3600.0 # arcsec

    fr_lon = grid(ts_lon, gridsize[0])
    fr_lat = grid(ts_lat, gridsize[1])
    sc_lon = np.tile(fr_lon, (len(ts_cur), 1))
    sc_lat = np.tile(fr_lat, (len(ts_cur), 1))
    ts_ilon = np.argmin(np.abs(sc_lon.T - ts_lon), axis=0)
    ts_ilat = np.argmin(np.abs(sc_lat.T - ts_lat), axis=0)

    mp_inp = np.zeros([len(fr_lat), len(fr_lon)])
    mp_cnt = np.zeros([len(fr_lat), len(fr_lon)])
    for t in range(len(ts_cur)):
        i, j = ts_ilat[t], ts_ilon[t]
        mp_inp[i,j] += ts_cur[t]
        mp_cnt[i,j] += 1.0

    mp_cur = mp_inp / np.ma.array(mp_cnt, mask=(mp_cnt==0.0))

    if '__vipar_currentmap__' in casaglobals.keys():
        mp_pre = casaglobals['__vipar_currentmap__']
        casaglobals['__vipar_previousmap__'] = mp_pre

    casaglobals['__vipar_currentmap__'] = mp_cur

    if show:
        lon, lat = np.meshgrid(fr_lon, fr_lat)
        fig = plt.figure(figsize=(8,6))
        ax0 = fig.add_subplot(111)
        ax0.set_aspect('equal')
        try:
            cmap = sns.cubehelix_palette(8, as_cmap=True)
            cax = ax0.pcolormesh(lon, lat, mp_cur, cmap=cmap)
        except:
            cax = ax0.pcolormesh(lon, lat, mp_cur)

        ax0.set_xlim([fr_lon.min(), fr_lon.max()])
        ax0.set_ylim([fr_lat.min(), fr_lat.max()])
        ax0.set_xlabel('Longitude Offset (arcsec)')
        ax0.set_ylabel('Latitude Offset (arcsec)')
        ax0.set_title('Pixel No.{}'.format(pixel))
        fig.colorbar(cax)
        plt.show()
