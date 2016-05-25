# coding: utf-8

import os
import sys
import inspect
from taskinit import *

def mbbaseline(mbfits=None, mode=None):
    casalog.origin('mbbaseline')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals
