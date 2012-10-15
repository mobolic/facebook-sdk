#!/usr/bin/env python
from distutils.core import setup

setup(
    name='facebook-sdk',
    version='0.4.0',
    description='This client library is designed to support the Facebook '
                'Graph API and the official Facebook JavaScript SDK, which '
                'is the canonical way to implement Facebook authentication.',
    author='Facebook',
    maintainer='Martey Dodoo',
    maintainer_email='facebook-sdk@marteydodoo.com',
    url='https://github.com/pythonforfacebook/facebook-sdk',
    license='Apache',
    py_modules=[
        'facebook',
    ],
    long_description=open("README.rst").read(),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
)
