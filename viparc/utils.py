# coding: utf-8

'''
tools.py - Vipar's utilities module

+ developer: Akio Taniguchi (IoA, UTokyo)
+ contact: taniguchi@ioa.s.u-tokyo.ac.jp
'''

# common preamble
import os
import sys
import inspect
import numpy as np

__mbnodef__ = '__mbnodef__'


def default(func):
    mbglobals = sys._getframe(1).f_globals

    name = func.func_code.co_name
    spec = inspect.getargspec(func)
    args = spec.args
    defs = spec.defaults or []
    values = []

    for i in range(len(args)-len(defs)):
        values.append(__mbnodef__)

    for i in range(len(defs)):
        values.append(defs[i])

    mbglobals['__mbsetfunc__'] = func

    for i in range(len(args)):
        mbglobals[args[i]] = values[i]

def go():
    mbglobals = sys._getframe(1).f_globals

    func = mbglobals['__mbsetfunc__']
    name = func.func_code.co_name
    spec = inspect.getargspec(func)
    args = spec.args
    kwargs = {}

    for arg in args:
        kwargs[arg] = mbglobals[arg]

    return func(**kwargs)

def inp():
    mbglobals = sys._getframe(1).f_globals

    func = mbglobals['__mbsetfunc__']
    name = func.func_code.co_name
    spec = inspect.getargspec(func)
    args = spec.args
    if len(args) > 0:
        npad = max([len(arg) for arg in args])

    print('{0}'.format(name))
    print('-'*len(name))

    for arg in args:
        value = mbglobals[arg]

        if value == __mbnodef__:
            value = '# no default value'
        elif type(value) == str:
            value = "'{0}'".format(value)

        print('- {0:<{1}} = {2}'.format(arg, npad, value))
