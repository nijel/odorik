Python module for Odorik API
============================

.. image:: https://travis-ci.org/nijel/odorik.svg?branch=master
    :target: https://travis-ci.org/nijel/odorik
    :alt: Build Status

.. image:: https://landscape.io/github/nijel/odorik/master/landscape.svg?style=flat
    :target: https://landscape.io/github/nijel/odorik/master
    :alt: Code Health

.. image:: http://codecov.io/github/nijel/odorik/coverage.svg?branch=master
    :target: http://codecov.io/github/nijel/odorik?branch=master
    :alt: Code coverage

.. image:: https://img.shields.io/pypi/dm/odorik.svg
    :target: https://pypi.python.org/pypi/odorik
    :alt: PyPI package

Documentation
-------------

See http://odorik.readthedocs.org/en/latest/ for module documentation.

See http://www.odorik.cz/w/api for API documentation.

Installation
------------

Use pip to install::

    pip install odorik

Command line utility
--------------------

The module comes with handy command line utility::

    $ odorik balance
    balance: 123.45

    $ odorik mobile-data --phone 00420789123456
    bytes_total: 111593707
    bytes_down: 87039672
    bytes_up: 24554035
    price: 0

    $ odorik send-sms 00420789123456 "Ahoj, jak se mas?"

See http://odorik.readthedocs.org/en/latest/command.html for more information.
