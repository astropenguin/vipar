# coding: utf-8

import os
import sys
import inspect
from datetime import datetime
from taskinit import casalog

def mbrecordscan(label=None):
    casalog.origin('mbrecordscan')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    if label == '':
        t_now = datetime.now()
        label = t_now.strftime('%Y%m%d%H%M%S')

    if not '__vipar_recorededscans__' in casaglobals.keys():
        casaglobals['__vipar_recorededscans__'] = {}

    sc_check = casaglobals['__vipar_currentscan__']
    casaglobals['__vipar_recorededscans__'][label] = sc_check
