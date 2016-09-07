# -*- coding: utf-8 -*-
"""Plot HATPRO timeseries.
"""
from clb import csv, plots
import matplotlib.pyplot as plt


t = {}
rh = {}
for week in [34, 35, 36]:
    csv.read_profile(
        'data/{}/RAD.txt'.format(week),
        var_regex='RAD_T\\d{5}',
        var_key='T_PROFILE',
        output=t)

    csv.read_profile(
        'data/{}/RAD.txt'.format(week),
        var_regex='RAD_RH\\d{5}',
        var_key='RH_PROFILE',
        output=rh)

fig, [ax1, ax2] = plt.subplots(2, 1)
pcm = ax1.pcolormesh(
    t['MPLTIME'],
    t['T_PROFILE_Z'] / 1e3,
    t['T_PROFILE'],
    cmap=plt.get_cmap('temperature', 10),
    rasterized=True)
ax1.set_ylabel('Höhe [km]')
ax1.set_xlabel('Datum')
plots.set_date_axis(ax1)
cb = fig.colorbar(pcm, ax=ax1)
cb.set_label('Temperatur [C]')

pcm = ax2.pcolormesh(
    rh['MPLTIME'],
    rh['RH_PROFILE_Z'] / 1e3,
    rh['RH_PROFILE'],
    cmap=plt.get_cmap('density', 10),
    rasterized=True)
ax2.set_ylabel('Höhe [km]')
ax2.set_xlabel('Datum')
plots.set_date_axis(ax2)
cb = fig.colorbar(pcm, ax=ax2)
cb.set_label('Relative Feuchte [%]')

fig.tight_layout()
fig.savefig('plots/hatpro.pdf')
