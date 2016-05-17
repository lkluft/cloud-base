# -*- coding: utf-8 -*-
"""Visualise the opacity within the frequency range of a pyrgeometer.

"""
import os

import numpy as np
import matplotlib.pyplot as plt
import typhon.cm
from typhon.arts import xml


f = xml.load('results/f_grid.xml')/1e12
z = xml.load('results/z_field.xml').flatten()
iy = xml.load('results/iy.xml')
iy_aux = xml.load('results/iy_aux.xml')

opacity = iy_aux[0].flatten()
abs_sum = iy_aux[1][:, 0, 0, :].T

plt.style.use('typhon')

# overall opacity
fig1, ax = plt.subplots()
ax.plot(f, opacity)
ax.plot(f, np.ones(f.size), color='k', linestyle='--')
ax.set_xlim(f.min(), f.max())
ax.set_xlabel('Frequenz [THz]')
ax.set_ylim(0.1, 2)
ax.set_ylabel('Optische Dicke')

# opacity in different heights
dz = np.diff(z)
abs_mean = (abs_sum[1:, :]+abs_sum[:-1, :]) / 2
z_mean = (z[1:]+z[:-1]) / 2
transmission = np.cumsum(abs_mean.T * np.diff(z), axis=1).T

fig2, ax = plt.subplots()
pcm = ax.pcolormesh(f, z_mean, transmission,
                    vmin=0,
                    vmax=1,
                    cmap='density',
                    rasterized=True)
ax.set_xlim(f.min(), f.max())
ax.set_xlabel('Frequenz [THz]')
ax.set_ylim(z_mean.min(), 8000)
ax.set_ylabel('Höhe [m]')
cb = fig2.colorbar(pcm)
cb.set_label('Optische Dicke')

fig1.savefig(os.path.join('plots', 'opacity.pdf'))
fig2.savefig(os.path.join('plots', 'transmission.pdf'))
