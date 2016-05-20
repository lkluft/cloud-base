# -*- coding: utf-8 -*-
"""Visualise radiative transfer results.
"""
from os.path import join

import numpy as np
import matplotlib.pyplot as plt
import typhon.cm
from typhon.arts import xml

import clb


f = xml.load(join('results', 'f_grid.xml'))
z = xml.load(join('results', 'z_field.xml')).flatten()
T_s = xml.load(join('results', 't_field.xml')).flatten()[0]
iy = xml.load(join('results', 'iy.xml')).flatten()
iy_aux = xml.load(join('results', 'iy_aux.xml'))

opacity = iy_aux[0].flatten()
abs_sum = iy_aux[1][:, 0, 0, :].T

## Calculations
# maximal detection height based on clear-sky ARTS run.
lwr = clb.integrate_spectrum(f, iy)

max_height = float(clb.estimate_cloud_height(lwr, T_s))
print('Maximal detection height: {:.0f}m'.format(max_height))


## Plots
f *= 1e-12  #convert to THz
plt.style.use('typhon')

# opacity in different heights
dz = np.diff(z)
abs_mean = (abs_sum[1:, :]+abs_sum[:-1, :]) / 2
z_mean = (z[1:]+z[:-1]) / 2
transmission = np.cumsum(abs_mean.T * np.diff(z), axis=1).T

fig1, ax1 = plt.subplots()
pcm = ax1.pcolormesh(f, z_mean, transmission,
                     vmin=0,
                     vmax=1,
                     cmap=plt.get_cmap('density', lut=10),
                     rasterized=True)
ax1.set_xlim(f.min(), f.max())
ax1.set_xlabel('Frequenz [THz]')
ax1.set_ylim(z_mean.min(), 8000)
ax1.set_ylabel('Höhe [m]')
cb = fig1.colorbar(pcm)
cb.set_label('Optische Dicke')

# radiance spectrum
fig2, ax2 = plt.subplots()
ax2.fill_between(f, clb.planck(f*1e12, T_s), color='lightgrey', label='Planck')
ax2.fill_between(f, iy, color='darkred', label='Messung')
ax2.legend()
ax2.set_xlim(f.min(), f.max())
ax2.set_xlabel('Frequenz [THz]')
ax2.set_ylabel(r'Radianz [$W\,m^{-2}\,sr^{-1}\,Hz^{-1}$]')

fig1.savefig(join('plots', 'opacity.pdf'))
fig2.savefig(join('plots', 'spectrum.pdf'))
