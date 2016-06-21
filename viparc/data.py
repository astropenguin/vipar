# coding: utf-8

'''
data.py - Vipar's database and data structure module

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
from copy import deepcopy
from datetime import datetime


class ViparDB(dict):
    def __init__(self, N_max=5):
        '''Vipar's mini database class.

        Args:
        - N_max (int): Maximum number of data that can be stored as history.
            default value is 5 (6th data will be deleted).
        '''
        dict.__init__(self)
        self.N_max = N_max

    def append(self, data):
        '''Append a new data to the database.

        Args:
        - data (object): a new data to be appended to the database

        Returns:
        this method returns nothing.
        '''
        indices = [i for i in self.keys() if type(i)==int]
        N_data = len(indices)

        if N_data == 0:
            pass

        elif 0 < N_data < self.N_max:
            for i in range(N_data)[::-1]:
                self[i+1] = self.pop(i)

        else:
            for i in range(N_data-1)[::-1]:
                self[i+1] = self.pop(i)

        self[0] = deepcopy(data)

    def pin(self, label=''):
        '''Pin the current data as labeled one.

        this data will not be deleted even if the number of data reaches N_max.

        Args:
        - label (str): a label of the new data. if not spacified (label=''),
            string of current datetime (YYYYmmddHHMMSS.ssssss) will be set.

        Returns:
        this method returns nothing.
        '''
        assert type(label) == str
        if label == '':
            label = datetime.now().strftime('%Y%m%d%H%M%S.%f')

        self[label] = deepcopy(self[0])

    def undo(self, label=''):
        '''Rewind the database to the previous or pinned state.

        Args:
        - label (str): a label of the pinned data to be returned.
            if not spacified (label=''), previous data will be set.

        Returns:
        this method returns nothing.
        '''
        indices = [i for i in self.keys() if type(i)==int]
        N_data = len(indices)

        assert type(label) == str
        if label == '':
            for i in range(N_data-1):
                self[i] = self.pop(i+1)

        else:
            self.append(self[label])

    def __getitem__(self, key):
        '''Overload the behavior of dict's __getitem__ method.

        Args:
        - key (str or int): key of the ViparDB.
            if key='', this returns self[0].

        Returns:
        - data (object): deepcopied value of self[key]
        '''
        if key == '':
            return deepcopy(dict.__getitem__(self, 0))
        else:
            return deepcopy(dict.__getitem__(self, key))


class MBScan(fits.HDUList):
    def __init__(self, hdus=[], file=None):
        fits.HDUList.__init__(self, hdus, file)

    @classmethod
    def fromfits(cls, f):
        mbsc = cls()

        sc = np.squeeze(f['arraydata-mbfits'].data.DATA)
        ts_mjd = f['datapar-mbfits'].data.MJD
        ts_daz = f['datapar-mbfits'].data.LONGOFF
        ts_del = f['datapar-mbfits'].data.LATOFF
        alist = [ts_mjd, ts_daz, ts_del]
        names = ['MJD', 'dAz', 'dEl']
        dtypes = ['f8', 'f8', 'f8']
        record = np.rec.fromarrays(alist, zip(names, dtypes))

        hdu_scan = fits.PrimaryHDU(sc)
        hdu_record = fits.BinTableHDU(record)

        hdu_scan.header['ORIGIN'] = os.path.basename(f.filename())
        hdu_scan.header['EXTNAME'] = 'DATA'
        hdu_record.header['EXTNAME'] = 'RECORD'

        mbsc.append(hdu_scan)
        mbsc.append(hdu_record)

        return mbsc

    @classmethod
    def frommap(cls):
        '''
        later implementation!
        '''
        pass

    def tomap(self, converter):
        mp, header = converter(self)
        record = self['record'].data

        return MBMap.fromscan(mp, header, record)

    def recordtask(self, taskname):
        if not 'TASKFLOW' in self['primary'].header.keys():
            self['data'].header['TASKFLOW'] = taskname
        else:
            self['data'].header['TASKFLOW'] += ' --> {0}'.format(taskname)


class MBMap(fits.HDUList):
    def __init__(self, hdus=[], file=None):
        fits.HDUList.__init__(self, hdus, file)

    @classmethod
    def fromscan(cls, mp, header, record):
        mbmp = cls()

        hdu_map = fits.PrimaryHDU(mp)
        hdu_record = fits.BinTableHDU(record)

        hdu_map.header['EXTNAME'] = 'DATA'
        hdu_map.header += header
        hdu_record.header['EXTNAME'] = 'RECORD'

        mbmp.append(hdu_map)
        mbmp.append(hdu_record)

        return mbmp

    def toscan(self, converter):
        '''
        later implementation!
        '''
        pass

    def getmeshgrid(self):
        h = self['data'].header
        grid_daz = h['CRVAL1'] + h['CDELT1']*(np.arange(h['NAXIS1'])+1-h['CRPIX1'])
        grid_del = h['CRVAL2'] + h['CDELT2']*(np.arange(h['NAXIS2'])+1-h['CRPIX2'])
        meshgrid = np.meshgrid(grid_daz, grid_del)

        return meshgrid

    def recordtask(self, taskname):
        if not 'TASKFLOW' in self['primary'].header.keys():
            self['data'].header['TASKFLOW'] = taskname
        else:
            self['data'].header['TASKFLOW'] += ' --> {0}'.format(taskname)
