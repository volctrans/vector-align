# -*- coding: utf-8 -*-
# create@ 2022-04-08 11:16

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

__project__ = 'vector-align'

stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s] - [%(levelname)s] - %(filename)s:%(lineno)d:\n%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
stream_handler.setFormatter(formatter)
logger = logging.getLogger(__project__)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
logger.propagate = False
