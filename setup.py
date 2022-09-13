# -*- coding: utf-8 -*-
# create@ 2022-04-03 12:33

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import os
from setuptools import find_packages, setup

NAME = 'vector_align'
DESCRIPTION = 'Production-ready tool for align parallel documents to sentences by vector similarity'
URL = 'https://code.byted.org/lab/vector-align'
EMAIL = ''
AUTHOR = ''

REQUIRES = [
    'requests',
    'pycld2',
    'polyglot',
    'Morfessor',
    'sentence-transformers'
]

DEV_REQUIRES = [
    'requests',
    'pycld2',
    'polyglot',
    'Morfessor',
    'sentence-transformers',
    'larksuite-oapi'
]


here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except IOError:
    long_description = DESCRIPTION


about = {}
with io.open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='vector,alignment',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=REQUIRES,
    include_package_data=True,
    tests_require=[
        'pytest>=4.0.0,<5.0.0'
    ],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    extras_require={
        ':python_version<"3.5"': [
            'typing>=3.6.4',
        ],
        'dev': DEV_REQUIRES,
    },
    package_data={
        # for PEP484 & PEP561
        NAME: ['py.typed', '*.pyi'],
    },
    entry_points={
            "console_scripts": [
                "vector-align=vector_align.main:main"
            ],
        },
)
