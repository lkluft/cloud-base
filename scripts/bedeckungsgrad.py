# -*- coding: utf-8 -*-
"""Estimate cloud cover by variation of incoming longwave radiation.
"""
import numpy as np
import matplotlib.pyplot as plt
import clb

master = clb.csv.read('/home/lukas/Desktop/2016/35/MASTER.txt')
cl = clb.csv.read('/home/lukas/Desktop/2016/35/CL.txt')

l_hourly = np.split(master['L'], 7 * 24)
master['L_STD'] = np.hstack([np.ones(60) * np.std(x) for x in l_hourly])

master['L_STD'] /= np.nanmax(master['L_STD'])
master['STD'] = master['L_STD']
cl['CL_SCBG'] /= 8

clb.math.compare_arrays(cl['CL_SCBG'], master['STD'], verbose=True)

# Plots
plt.style.use('typhon')

fig, ax = plt.subplots()
clb.plots.time_series(cl, 'CL_SCBG', label='Ceilometer', linewidth=4)
clb.plots.time_series(master, 'STD', label='Pyrgeometer',
                      linewidth=4, color='darkorange')
ax.set_ylabel('Bedeckungsgrad')
ax.set_ylim(0, 1.2)
fig.savefig('plots/bedeckungsgrad.pdf')

fig, ax = plt.subplots()
x = np.linspace(0, 1, 15)
y = np.linspace(0, 1, 9)
N, x, y, img = ax.hist2d(
    master['STD'],
    cl['CL_SCBG'],
    (x, y),
    cmap=plt.get_cmap('speed', 20))
ax.set_xlabel('Normierte Standardabweichung L')
ax.set_ylabel('Bedeckungsgrad')
ax.set_aspect('equal')
fig.colorbar(img, label='Anzahl')
fig.savefig('plots/std_bedeckung_correlation.pdf')
