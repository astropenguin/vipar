# coding: utf-8

import os
import sys
import inspect
from taskinit import *

def mbnoiseremoval(mbfits=None, mode=None):
    casalog.origin('mbnoiseremoval')
    casaglobals = sys._getframe(len(inspect.stack())-1).f_globals
