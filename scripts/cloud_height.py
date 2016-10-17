# -*- coding: utf-8 -*-
"""Estimate the cloud base height using measurements of
longwave radiation and 2m temperature.

"""
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import typhon.plots
import clb


def main(mfilename, cfilename):
    """Main function."""
    data = clb.csv.read(mfilename, variables=['L', 'TT002'])
    clb.csv.read_scat(cfilename, output=data)

    date = data['MPLTIME']
    lwr = data['L']
    T_s = data['TT002'] + 273.15
    z = data['CLB_MATRIX_Z']
    back_scat = data['CLB_MATRIX']

    data['CBH'] = clb.estimate_cloud_height(lwr, T_s)

    plt.style.use(typhon.plots.styles('typhon'))

    # LWR time series
    fig1, ax1 = plt.subplots(figsize=(20, 6))
    clb.plots.plot_lwr(data, ax=ax1)

    # brightness temperature time series
    fig2, ax2 = plt.subplots(figsize=(20, 6))
    data['T_B'] = (
        clb.physics.irradiance2temperature(lwr) -
        clb.physics.irradiance2temperature(clb.lwr_surrounding(T_s)))
    clb.plots.plot_T_b(data, ax=ax2)

    # back scattering and CLB
    fig3, ax3 = plt.subplots(figsize=(20, 6))
    clb.plots.plot_back_scat(date, z, back_scat, ax=ax3)
    clb.plots.plot_clb(data, ax=ax3)

    fig1.savefig(os.path.join('plots', 'lwr.pdf'))
    fig2.savefig(os.path.join('plots', 't_b.pdf'))
    fig3.savefig(os.path.join('plots', 'clb.pdf'), dpi=600)

if __name__ == '__main__':
    main('data/35/MASTER.txt', 'data/35/CLB.txt')
