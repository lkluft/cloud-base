# -*- coding: utf-8 -*-
"""Evluate the influence of the elevation angle when simulating incoming
longwave radiation.
"""
import numpy as np
import matplotlib.pyplot as plt
import clb
from typhon.arts import xml
from typhon.plots import styles


f = xml.load('../arts/results/angle_integration/f_grid.xml')
y_los = xml.load('../arts/results/angle_integration/y.xml')
los = xml.load('../arts/results/angle_integration/sensor_los.xml')

plt.style.use(styles('typhon'))

lwr_new = clb.math.integrate_angles(f, y_los, los, dtheta=15)

fig, ax = plt.subplots()
for y, a in zip(np.split(y_los, los.size), los):
    ax.plot(f/1e12, y,
            label='${}^\circ$'.format(int(a)),
            linewidth=3,
            linestyle='-')
ax.set_xlim(f.min()/1e12, f.max()/1e12)
ax.set_xlabel('Frequenz [THz]')
ax.set_ylabel(r'Radianz [$W\,m^{-2}\,sr^{-1}\,Hz^{-1}$]')
ax.legend(ncol=2)
fig.savefig('plots/lwr_spectrum_elevation.pdf')
