# coding: utf-8

import os
import sys
import inspect
from datetime import datetime
from taskinit import casalog

def mbrecordmap(label=None):
    casalog.origin('mbrecordmap')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    if label == '':
        t_now = datetime.now()
        label = t_now.strftime('%Y%m%d%H%M%S')

    if not '__vipar_recordedmaps__' in casaglobals.keys():
        casaglobals['__vipar_recordedmaps__'] = {}

    mp_check = casaglobals['__vipar_currentmap__']
    casaglobals['__vipar_recordedmaps__'][label] = mp_check
