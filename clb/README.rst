================
Cloud Base (clb)
================

clb provides functions to read CSV files using the Wettermast format and to
easily plot atmospheric time series.

The top level package provides additional functions to estimate the cloud base
height from measured long wave radiation and near-surface temperature.

Installation
============

If you are using Anaconda (highly recommended) you can create an environment
called cloud-base with all required depencies by executing following command in
this directory.

    conda env create

Afterwards you can install this package without the need for dependencies.

    pip install --no-deps -e .

If your are not using Anaconda you can run

    pip install -e .

Structure
=========

csv
---

Functions to estimate the cloud base height.

csv.csv
^^^^^^^

csv provides functionality to comfortably read CSV files.

csv.plots
^^^^^^^^^

plots provides plotting routines to perform basic time series plots
conveniently.
