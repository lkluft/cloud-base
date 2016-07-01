#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Estimate the cloud base height using measurements
of longwave radiation and 2m temperature.
"""
import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import clb


def main(mfilename, cfilename):
    """Main function."""
    data = clb.csv.read(mfilename, variables=['L', 'TT002'])
    clb.csv.read_scat(cfilename, output=data)

    date = data['MPLTIME']
    lwr = data['L']
    T_s = data['TT002'] + 273.15
    z = data['CLB_Z']
    back_scat = data['CLB_MATRIX']

    cloud_height = clb.estimate_cloud_height(lwr, T_s)

    try:
        plt.style.use('typhon')
    except:
        plt.style.use('seaborn-poster')

    # LWR time series
    fig1, ax1 = plt.subplots(figsize=(20, 6))
    clb.plots.plot_lwr(date, lwr, ax=ax1)

    # brightness temperature time series
    fig2, ax2 = plt.subplots(figsize=(20, 6))
    dT_b = clb.lwr_to_T_b(lwr) - clb.lwr_to_T_b(clb.lwr_surrounding(T_s))
    clb.plots.plot_T_b(date, dT_b, ax=ax2)

    # back scattering and CLB
    fig3, ax3 = plt.subplots(figsize=(20, 6))
    clb.plots.plot_back_scat(date, z, back_scat, ax=ax3)
    clb.plots.plot_clb(date, cloud_height, ax=ax3)

    fig1.savefig(os.path.join('plots', 'lwr.pdf'))
    fig2.savefig(os.path.join('plots', 't_b.pdf'))
    fig3.savefig(os.path.join('plots', 'clb.pdf'), dpi=600)

if __name__ == '__main__':
    main('data/MASTER.txt', 'data/CLB.txt')
