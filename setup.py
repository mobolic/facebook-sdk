#!/usr/bin/env python
from distutils.core import setup
 
setup(
    name='facebook-sdk',
    version='0.3.0',
    description='This client library is designed to support the Facebook Graph API and the official Facebook JavaScript SDK, which is the canonical way to implement Facebook authentication.',
    author='Kit Sunde',
    author_email='kitsunde@gmail.com',
    url='http://github.com/Celc/facebook-sdk',
    package_dir={'': 'src'},
    py_modules=[
        'facebook',
    ],
)