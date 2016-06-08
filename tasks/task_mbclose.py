# coding: utf-8

import os
import sys
import inspect
from taskinit import casalog

def mbclose():
    casalog.origin('mbclose')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals

    if '__vipar_mbfits__' in casaglobals.keys():
        casaglobals['__vipar_mbfits__'].close()

    if '__vipar_scans__' in casaglobals.keys():
        del casaglobals['__vipar_scans__']

    if '__vipar_maps__' in casaglobals.keys():
        del casaglobals['__vipar_maps__']
