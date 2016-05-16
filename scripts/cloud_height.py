#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Estimate the cloud basis height using measurements of longwave radtion.
"""

import numpy as np
import matplotlib.pyplot as plt

import clb
import clb.csv as csv
import clb.plots as plots


def main():
    """Main function."""
    data = clb.csv.read_master('MASTER.txt')
    date = clb.csv.read_mpl_date('MASTER.txt')
    ceilo = clb.csv.read_ceilo('CLB.txt')
    lwr = data['L']
    T_s = np.nanmean(data['TT002'])

    h = np.linspace(0, 10000, 500)

    T_b = clb.lwr_to_temperature(lwr)
    T_a = clb.standard_atmosphere(h, T_s=T_s)

    foo = np.array([clb.find_value(h, T_a, t) for t in T_b])


    plt.plot(date, data['TT002'])
    plots.plot_lwr(date, lwr)
    fig, ax = plots.plot_ceilo(date, ceilo['z'], ceilo['back_scat'])
    ax.plot(date, foo, color='orange', linewidth=2)
    plt.show()


if __name__ == '__main__':
    main()
