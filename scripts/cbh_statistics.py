# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import matplotlib.pyplot as plt
import clb
from clb import csv, plots

data = csv.read('/home/lukas/Desktop/2016/35/CL.txt')
csv.read('/home/lukas/Desktop/2016/35/MASTER.txt', stack=False, output=data)

data['PYR_CBH'] = clb.estimate_cloud_height(data['L'], data['TT002']+273.15)

# 10 minute moving average
_, data['PYR_CBH'] = clb.math.moving_average(
                         data['MPLTIME'], data['PYR_CBH'], 10)
_, data['CL_WBU'] = clb.math.moving_average(
                         data['MPLTIME'], data['CL_WBU'], 10)

# Statistics of both time series
stats = clb.math.compare_arrays(data['CL_WBU'], data['PYR_CBH'], verbose=True)


# Plot time series.
plt.style.use('typhon')

fig, ax = plt.subplots()
for var in ['CL_WBU', 'PYR_CBH']:
    plots.time_series(data, var, ylabel='Wolkenbasishöhe [m]')
ax.legend()
fig.savefig('plots/cbh_time_series.pdf')

# Plot correltion heatmap.
fig, ax = plt.subplots()
xedges = yedges = np.arange(0, 4000, 400)
N, x, y, img = ax.hist2d(data['CL_WBU'],
                         data['PYR_CBH'],
                         (xedges, yedges),
                         cmap='Greys')
ax.set_aspect('equal')
fig.colorbar(img)
fig.savefig('plots/cbh_correlation.pdf')
