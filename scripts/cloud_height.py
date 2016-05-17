#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Estimate the cloud basis height using measurements of longwave radtion.
"""
import os

import numpy as np
import matplotlib.pyplot as plt

import clb
import clb.csv as csv
import clb.plots as plots


def main(mfilename, cfilename):
    """Main function."""
    date = clb.csv.read_mpl_date(mfilename)

    data = clb.csv.read_master(mfilename)
    lwr = data['L']
    T_s = data['TT002'] + 273.15

    back_scat, z = clb.csv.read_ceilo(cfilename)

    T_b = clb.lwr_to_T_b(lwr) - clb.lwr_to_T_b(clb.lwr_surrounding(T_s))

    cloud_height = T_b / -0.0065

    try:
        plt.style.use('typhon')
    except:
        plt.style.use('seaborn-poster')

    # LWR time series
    fig1, ax = plots.plot_lwr(date, lwr)

    # brightness temperature time series
    fig2, ax = plots.plot_brightness_t(date, T_b)

    # back scattering and estimated CLB
    fig3, ax = plots.plot_ceilo(date, z, back_scat)
    ax.plot(date, cloud_height,
            color='orange',
            linewidth=2,
            label='Wolkenhöhe')
    ax.legend()

    fig1.savefig(os.path.join('plots', 'lwr.pdf'))
    fig2.savefig(os.path.join('plots', 'brightness_temperature.pdf'))
    fig3.savefig(os.path.join('plots', 'clb_improved.pdf'))

if __name__ == '__main__':
    main('data/MASTER2.txt', 'data/CLB2.txt')
