# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import matplotlib.pyplot as plt
import clb
from clb import csv, plots
from typhon.plots import figsize


data = csv.read('/home/lukas/Desktop/2016/35/CL.txt')
csv.read('/home/lukas/Desktop/2016/35/MASTER.txt', stack=False, output=data)

data['PYR_CBH'] = clb.estimate_cloud_height(data['L'], data['TT002']+273.15)

# 10 minute moving average
_, data['PYR_CBH'] = clb.math.moving_average(
                         data['MPLTIME'], data['PYR_CBH'], 10)
_, data['CL_WBU'] = clb.math.moving_average(
                         data['MPLTIME'], data['CL_WBU'], 10)

# Plots
plt.style.use('typhon')

fig, axes = plt.subplots(4, 2, figsize=figsize(15), sharex=True, sharey=True)
for cc, ax in zip(np.arange(1, 9), axes.ravel()):
    # mask = np.logical_and(data['CL_SCBG'] >= cc , data['CL_SCBG'] < cc + 1)
    mask = np.logical_and(np.ma.greater_equal(data['CL_SCBG'], cc),
                          np.ma.less(data['CL_SCBG'], cc + 1))

    sts = clb.math.compare_arrays(data['CL_WBU'][mask], data['PYR_CBH'][mask])

    ax.plot(
        data['MPLTIME'][mask],
        data['CL_WBU'][mask]/1e3,
        color='darkblue',
        label='Ceilometer',
        linestyle='none',
        marker='.')
    ax.plot(
        data['MPLTIME'][mask],
        data['PYR_CBH'][mask]/1e3,
        color='darkorange',
        label='Pyrgeometer',
        linestyle='none',
        marker='.')

    if ax.is_first_col():
        ax.set_ylabel('CBH [km]')

    if ax.is_last_row():
        ax.set_xlabel('Datum')

    if ax.is_first_row() and ax.is_first_col():
        ax.legend(ncol=2)

    clb.plots.set_date_axis(ax=ax)
    ax.set_ylim(0, 6)
    ax.set_title('Bedeckung {:.0f}/8, r = {:.2f}'.format(
        cc, sts.corrcoef))

fig.tight_layout()
fig.savefig('plots/cbh_cloud_cover.pdf')

fig, axes = plt.subplots(4, 2, figsize=figsize(15), sharex=True, sharey=True)
cloud_heights = np.linspace(0, 6000, 9)
for i, ax in enumerate(axes.ravel()):
    # mask = np.logical_and(data['CL_WBU'] > cloud_heights[i],
    #                       data['CL_WBU'] <= cloud_heights[i + 1])
    mask = np.logical_and(
                np.ma.greater(data['CL_WBU'], cloud_heights[i]),
                np.ma.less_equal(data['CL_WBU'], cloud_heights[i + 1])
                )

    sts = clb.math.compare_arrays(data['CL_WBU'][mask], data['PYR_CBH'][mask])

    ax.plot(
        data['MPLTIME'][mask],
        data['CL_WBU'][mask]/1e3,
        color='darkblue',
        label='Ceilometer',
        linestyle='none',
        marker='.')
    ax.plot(
        data['MPLTIME'][mask],
        data['PYR_CBH'][mask]/1e3,
        color='darkorange',
        label='Pyrgeometer',
        linestyle='none',
        marker='.')

    if ax.is_first_col():
        ax.set_ylabel('CBH [km]')

    if ax.is_last_row():
        ax.set_xlabel('Datum')

    if ax.is_first_row() and ax.is_first_col():
        ax.legend(ncol=2)

    clb.plots.set_date_axis(ax=ax)
    ax.set_ylim(0, 6)
    ax.set_title('Höhe {:.0f}-{:.0f}m, r = {:.2f}'.format(
        cloud_heights[i], cloud_heights[i + 1], sts.corrcoef))

fig.tight_layout()
fig.savefig('plots/cbh_cloud_height.pdf')

# Calculate and plot the full correltion matrix
cloud_cover = np.arange(1, 9)
cloud_heights = np.linspace(0, 6000, 9)
corr = np.zeros((cloud_cover.size, cloud_heights.size - 1))

for j, cc in enumerate(cloud_cover):
    for i in range(cloud_heights.size - 1):    
        lm1 = np.logical_and(np.ma.greater_equal(data['CL_SCBG'], cc),
                          np.ma.less(data['CL_SCBG'], cc + 1))

        lm2 = np.logical_and(
                np.ma.greater(data['CL_WBU'], cloud_heights[i]),
                np.ma.less_equal(data['CL_WBU'], cloud_heights[i + 1])
                )
        
        mask = np.logical_and(lm1, lm2)        
        
        # Require at lest 20 matches.
        if np.sum(mask) > 20:        
            sts = clb.math.compare_arrays(data['CL_WBU'][mask],
                                      data['PYR_CBH'][mask])

            corr[j, i] = sts.corrcoef 
        else:
            corr[j, i] = np.nan

fig, ax = plt.subplots()
pcm = ax.pcolormesh(np.arange(0, 9),
                    cloud_heights[::-1],
                    np.ma.masked_invalid(corr),
                    cmap=plt.get_cmap('difference', 15),
                    vmin=-1,
                    vmax=1,
                    rasterized=True)
ax.set_xlabel(r'Bedeckung [Achtel]')
ax.set_ylabel('Wolkenhöhe [m]')
fig.colorbar(pcm, label='Korrelation')
fig.savefig('plots/cbh_correlation_matrix.pdf')

# Statistics of both time series
sts = clb.math.compare_arrays(data['CL_WBU'], data['PYR_CBH'], verbose=True)

fig, ax = plt.subplots()
plots.time_series(data, 'CL_WBU',
                  ylabel='Wolkenbasishöhe [m]',
                  label='Ceilometer',
                  color='darkblue')
plots.time_series(data, 'PYR_CBH',
                  ylabel='Wolkenbasishöhe [m]',
                  label='Pyrgeometer',
                  color='darkorange')
ax.legend()
ax.set_ylim(0, 6000)
fig.savefig('plots/cbh_time_series.pdf')

# Plot correltion heatmap.
fig, ax = plt.subplots()
xedges = yedges = np.arange(0, 4000, 300)
N, x, y, img = ax.hist2d(data['CL_WBU'],
                         data['PYR_CBH'],
                         (xedges, yedges),
                         cmap=plt.get_cmap('Greys', 10))
ax.plot(x, y, color='r', linestyle='dashed')
ax.set_title('RMSE = {:.0f}m,r = {:.2f}'.format(sts.rmse, sts.corrcoef))
ax.set_xlabel('Ceilometer CBH [m]')
ax.set_ylabel('Pyrgeometer CBH [m]')
ax.set_aspect('equal')
fig.colorbar(img, label='Anzahl')
fig.savefig('plots/cbh_correlation.pdf')
