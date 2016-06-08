# coding: utf-8

from copy import deepcopy
from datetime import datetime

class ViparDB(dict):
    def __init__(self, N_max=10):
        '''Vipar's database class.

        Parameters
        ----------
        + N_max (int): maximum number of data that can be stored.
                       default value: 10.
        '''
        dict.__init__(self)
        self.N_max = N_max

    def append(self, data):
        '''append a new data to the database.

        Parameters
        ----------
        + data (array): a new data to be appended to the database

        Returns
        ----------
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

    def record(self, label=None):
        '''record the current data as labeled one. this data will
        not be deleted even if the number of data reaches N_max.

        Parameters
        ----------
        + label (str): a label of the new data. if not spacified, string
                       of current datetime (YYYYmmddHHMMSS) will be set.

        Returns
        ----------
        this function returns nothing.
        '''
        if (label is None) or (label == ''):
            label = datetime.now().strftime('%Y%m%d%H%M%S')

        assert type(label) == str
        self[label] = deepcopy(self[0])

    def undo(self, label=None):
        '''rewind the database to the previous or recorded state.

        Parameters
        ----------
        + label (str): a label of the recorded data to be returned.
                       if not spacified, previous data will be set.

        Returns
        ----------
        this function returns nothing.
        '''
        indices = [i for i in self.keys() if type(i)==int]
        N_data = len(indices)

        if (label is None) or (label == ''):
            for i in range(N_data-1):
                self[i] = self.pop(i+1)

        else:
            self.append(self[label])
