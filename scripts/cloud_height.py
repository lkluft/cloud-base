#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Estimate the cloud base height using measurements
of longwave radtion and 2m temperature.
"""
import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import clb
from clb import csv
from clb import  plots


def main(mfilename, cfilename):
    """Main function."""
    date = clb.csv.read_mpl_date(mfilename)

    data = clb.csv.read_master(mfilename)
    lwr = data['L']
    T_s = data['TT002'] + 273.15

    back_scat, z = clb.csv.read_scat(cfilename)

    T_b = clb.lwr_to_T_b(lwr) - clb.lwr_to_T_b(clb.lwr_surrounding(T_s))

    cloud_height = T_b / -0.0065

    try:
        plt.style.use('typhon')
    except:
        plt.style.use('seaborn-poster')

    # LWR time series
    fig1, ax1 = plt.subplots(figsize=(20, 6))
    plots.plot_lwr(date, lwr, ax=ax1)

    # brightness temperature time series
    fig2, ax2 = plt.subplots(figsize=(20, 6))
    plots.plot_T_b(date, T_b, ax=ax2)

    # back scattering and estimated CLB
    fig3, ax3 = plt.subplots(figsize=(20, 6))
    plots.plot_ceilo(date, z, back_scat, ax=ax3)
    ax3.plot(date, cloud_height,
             color='darkorange',
             alpha=0.7,
             linewidth=2,
             label='Wolkenhöhe')
    ax3.legend()

    fig1.savefig(os.path.join('plots', 'lwr.pdf'))
    fig2.savefig(os.path.join('plots', 't_b.pdf'))
    fig3.savefig(os.path.join('plots', 'clb.pdf'))

if __name__ == '__main__':
    main('data/MASTER2.txt', 'data/CLB2.txt')
