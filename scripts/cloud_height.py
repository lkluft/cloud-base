#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Estimate the cloud basis height using measurements of longwave radtion.
"""

import numpy as np
import matplotlib.pyplot as plt

import clb
import clb.csv as csv
import clb.plots as plots


def main(mfilename, cfilename):
    """Main function."""
    data = clb.csv.read_master(mfilename)
    date = clb.csv.read_mpl_date(mfilename)
    back_scat, z = clb.csv.read_ceilo(cfilename)
    lwr = data['L']
    T_s = data['TT002']

    T_b = clb.lwr_to_temperature(lwr)
    T_a = clb.lapse_rate(T_s, z) + 273.15

    tt_b, zz = np.meshgrid(T_b, z)

    # TODO: Need to get indexing clear. Why does the diagonal() thing work?
    cloud_height = zz[np.abs(tt_b - T_a).argmin(axis=0)].diagonal()

    plt.style.use('typhon')
    fig, ax = plots.plot_ceilo(date, z, back_scat)
    ax.plot(date, cloud_height, color='orange', linewidth=2, label='Wolkenhöhe')
    ax.legend()
    fig.savefig(cfilename.replace('.txt', '.pdf'))


if __name__ == '__main__':
    main('data/MASTER.txt', 'data/CLB.txt')
