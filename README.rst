========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-depp/badge/?style=flat
    :target: https://readthedocs.org/projects/python-depp
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/seddonym/python-depp.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/seddonym/python-depp

.. |version| image:: https://img.shields.io/pypi/v/depp.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/depp

.. |commits-since| image:: https://img.shields.io/github/commits-since/seddonym/python-depp/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/seddonym/python-depp/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/depp.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/depp

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/depp.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/depp

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/depp.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/depp


.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install depp

Documentation
=============


https://python-depp.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
