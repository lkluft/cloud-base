# -*- coding: utf-8 -*-
#
# Copyright © 2016 Lukas Kluft <lukas.kluft@gmail.com>
#
# Distributed under terms of the MIT license.

"""
Plot HATPRO timeseries.
"""
from clb import csv, plots
import matplotlib.pyplot as plt


data = csv.read_profile('data/RAD.txt', var_regex='RAD_T\\d{5}', var_key='T_PROFILE')
csv.read_profile('data/RAD.txt', var_regex='RAD_RH\\d{5}', var_key='RH_PROFILE', output=data)

fig, [ax1, ax2] = plt.subplots(2, 1)
pcm = ax1.pcolormesh(data['MPLTIME'], data['T_PROFILE_Z'] / 1e3, data['T_PROFILE'],
                     cmap=plt.get_cmap('temperature', 10),
                     rasterized=True)
ax1.set_ylabel('Höhe [km]')
plots.set_date_axis(ax1)
cb = fig.colorbar(pcm, ax=ax1)
cb.set_label('Temperature [C]')

pcm = ax2.pcolormesh(data['MPLTIME'], data['RH_PROFILE_Z'] / 1e3, data['RH_PROFILE'],
                     cmap=plt.get_cmap('density', 10),
                     rasterized=True)
ax2.set_ylabel('Höhe [km]')
plots.set_date_axis(ax2)
cb = fig.colorbar(pcm, ax=ax2)
cb.set_label('Relative Feuchte [%]')

fig.tight_layout()
fig.savefig('plots/hatpro.pdf')
