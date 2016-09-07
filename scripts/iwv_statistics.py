# -*- coding: utf-8 -*-
"""Statistical analysis of the Integrated Water Vapor retrieval.
"""
import numpy as np
import matplotlib.pyplot as plt
import clb


data = clb.csv.read('data/iwv.txt')

rad = np.ma.masked_greater(data['RAD_IWV'], 60)
pyr = data['PYR_IWV']

window = []
corr = []
for w in np.arange(1, 36):
    _, pyr_mean = clb.math.moving_average(np.zeros(pyr.size), pyr, w)
    stats = clb.math.compare_arrays(rad, pyr_mean, verbose=False)
    window.append(w)
    corr.append(stats.corrcoef)

_, pyr = clb.math.moving_average(
             np.zeros(pyr.size), pyr, window[np.argmax(corr)])
offset = np.nanmean(pyr - rad)

clb.math.compare_arrays(rad, pyr, verbose=True)

plot_data = {
    'MPLTIME': data['MPLTIME'],
    'Radiometer': rad,
    'Pyrgeometer': data['PYR_IWV'],
    'Pyrgeometer Mittel': pyr
    }

fig, ax = plt.subplots()
clb.plots.time_series(
    plot_data,
    ['Radiometer', 'Pyrgeometer', 'Pyrgeometer Mittel'],
    ylabel=r'Wasserdampfsäule [$g\,m^{-2}$]'
    )
fig.savefig('plots/iwv_smoothing.pdf')

fig, ax = plt.subplots()
x = y = np.linspace(10, 50, 25)
N, x, y, img = ax.hist2d(rad, pyr, (x, y), cmap='Greys')
ax.plot(x, y, color='r', linestyle='dashed')
ax.set_xlabel(r'Radiometer IWV [$g\,m^{-2}$]')
ax.set_ylabel(r'Pyrgeometer IWV [$g\,m^{-2}$]')
ax.set_xlim(x.min(), x.max())
ax.set_ylim(y.min(), y.max())
ax.set_aspect('equal')
fig.colorbar(img, label='Anzahl')
fig.savefig('plots/iwv_correlation.pdf')


w, c = 10 * np.array(window), np.array(corr)
fig, ax = plt.subplots()
ax.plot(w, c)
ax.set_xlim(w.min(), w.max())
ax.set_xlabel('Mittelungsintervall [min]')
ax.set_ylabel('Korrelationskoeffizient')
fig.savefig('plots/correlation_smoothing.pdf')
