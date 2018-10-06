============
Installation
============

The SDK currently supports Python 2.7 and Python 3.4-3.7. The `requests`_
package is required.

We recommend using `pip`_ and `virtualenv`_ to install the SDK. Please note
that the SDK's Python package is called **facebook-sdk**.

Installing from Git
===================

For the newest features, you should install the SDK directly from Git.

.. code-block:: shell

    virtualenv facebookenv
    source facebookenv/bin/activate
    pip install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk

Installing a Released Version
=============================

If your application requires maximum stability, you will want to use a version
of the SDK that has been officially released.

.. code-block:: shell

    virtualenv facebookenv
    source facebookenv/bin/activate
    pip install facebook-sdk

.. _requests: https://pypi.python.org/pypi/requests
.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/
