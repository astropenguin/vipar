# coding: utf-8

'''
log.py - Vipar's logging module

+ developer: Akio Taniguchi (IoA, UTokyo)
+ contact: taniguchi@ioa.s.u-tokyo.ac.jp
'''

import os
import logging
from datetime import datetime

config = {}
config['level'] = logging.INFO
config['format'] = '%(asctime)s  %(levelname)-6s  %(name)-18s  %(message)s'
config['datefmt'] = '%Y-%m-%d %H:%M:%S'
config['filename'] = 'vipar-{:%Y%m%d-%H%M%S}.log'.format(datetime.now())
logging.basicConfig(**config)

# naming style of this class is exceptionally non-CamelCase
# because the corresponding logging class in CASA is "casalog"
class pythonlog(object):
    '''Vipar's logging class.

    This only works when Vipar is used outside CASA (development use).
    Normally logs are recorded by the CASA logger (using casalog class).

    Examples:
    >>> from viparc.log import pythonlog as logger
    >>> logger.origin('mbopenfits')
    2016-06-13 18:16:15  INFO    mbopenfits  ----------

    >>> logger.post('the spacified MBFITS is not found', 'ERROR')
    2016-06-13 18:16:30  ERROR   mbopenfits  the spacified MBFITS is not found'
    '''
    name = 'root'

    @classmethod
    def origin(cls, fromwhere):
        cls.name = fromwhere
        logger = logging.getLogger(cls.name)
        logger.info('-'*50)

    @classmethod
    def post(cls, message, priority='INFO'):
        logger = logging.getLogger(cls.name)
        getattr(logger, priority.lower())(message)
