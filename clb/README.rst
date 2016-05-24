================
Cloud Base (clb)
================

clb provides functions to read CSV files using the Wettermast format and to
easily plot atmospheric time series.

The top level package provides additional functions to estimate the cloud base
height from measured long wave radiation and near-surface temperature.

Installation
============

If you are using `Anaconda <https://www.continuum.io/downloads>`_ (highly
recommended) you can create an environment called ``cloud-base`` with all
dependencies required in ``environment.yml``.

To do this simply run the following command in this directory.

    conda env create

Afterwards it is sufficient to install the package with ``pip``.

    pip install --user --no-deps -e .

Structure
=========

clb
---
Functions to estimate the cloud base height.

clb.csv
^^^^^^^
Load CSV files stored in Wettermast format.

clb.plots
^^^^^^^^^
Plot basic atmospheric properties conveniently.
