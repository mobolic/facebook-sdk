#!/usr/bin/env python
from distutils.core import setup

setup(
    name='facebook-sdk',
    version='0.5.0',
    description='This client library is designed to support the Facebook '
                'Graph API and the official Facebook JavaScript SDK, which '
                'is the canonical way to implement Facebook authentication.',
    author='Facebook',
    maintainer='Mantas Vidutis',
    maintainer_email='facebook-sdk@vidutis.com',
    url='https://github.com/mvid/facebook-sdk',
    license='Apache',
    py_modules=[
        'facebook',
    ],
    long_description=open("README.rst").read(),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
)
