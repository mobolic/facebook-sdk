#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
 
setup(
    name='facebook-python-sdk',
    version='0.1.2',
    description='This client library is designed to support the Facebook Graph API and the official Facebook JavaScript SDK, which is the canonical way to implement Facebook authentication.',
    author='Facebook',
    url='http://github.com/facebook/python-sdk',
    package_dir={'': 'src'},
    py_modules=[
        'facebook',
    ],
)
