# -*- coding: utf-8 -*-
"""Retrieve the integrate water vapor path (IWP) through longwave radiation
measurements.

"""
import clb
import typhon
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typhon.arts import xml, atm_fields_compact_get


atmospheres = xml.load('/home/lukas/arts-xml-data/planets/Earth/ECMWF/IFS/Chevallier_91L/chevallierl91_all_full.xml.gz')
ybatch = xml.load('../arts/results/angles/ybatch.xml')
f = xml.load('../arts/results/angles/f_grid.xml')
los = xml.load('../arts/results/angles/sensor_los.xml')


def integrate_angles(f, y_los, los):
    """Integrate spectrum over frequency and angles.

    Parameters:
        f: Frequency grid [Hz].
        y_los: Concatenated spectra for all angles.
        los: Viewing angles.

    Retuns:
        Integrated spectrum [W/m**2].

    """
    y_int = np.zeros(f.size)
    for y, a in zip(np.split(y_los, los.size), los):
        y_int += np.cos(np.deg2rad(a)) * y * np.deg2rad(15)
    return clb.integrate_spectrum(f, y_int)


iwv = np.zeros(len(atmospheres))
lwr = np.zeros(len(ybatch))
for i in range(len(atmospheres)):
    z, T, q = atm_fields_compact_get(
        ['z', 'T', 'abs_species-H2O'],
        atmospheres[i])
    p = atmospheres[i].grids[1]
    iwv[i] = typhon.atmosphere.iwv(q.ravel(), p, T.ravel(), z.ravel())
    lwr[i] = integrate_angles(f, ybatch[i], los)

# IWP and LWR correlation (ARTS simulation)
N, x, y = np.histogram2d(iwv, lwr, (25, 25))

plt.style.use('typhon')

fig, ax = plt.subplots()
pcm = ax.pcolormesh(x, y, N.T,
                    cmap=plt.get_cmap('cubehelix_r'),
                    rasterized=True)
ax.set_title('r = {:.3f}'.format(np.corrcoef(iwv, lwr)[0, 1]))
ax.set_xlim(0, x.max())
ax.set_ylim(y.min(), y.max())
ax.set_ylabel(r'Langwellige Einstrahlung [$Wm^{-2}$]')
ax.set_xlabel('Wasserdampfsäule [$kg\,m^{-2}$]')
cb = fig.colorbar(pcm)
cb.set_label('Anzahl')
fig.savefig('plots/iwv_lwr_correlation.pdf')


# Fit IWV(LWR).
def IWV(dT, a, b, c):
    return a * np.exp(b * dT) + c


popt, pcov = curve_fit(IWV, lwr, iwv, p0=[10, 0.001, 0])

fig, ax = plt.subplots()
N, x, y = np.histogram2d(lwr, iwv, (25, 25))
pcm = ax.pcolormesh(x, y, N.T,
                    cmap=plt.get_cmap('density', 8),
                    rasterized=True)
x = np.linspace(lwr.min(), lwr.max(), 100)
ax.plot(x, IWV(x, *popt),
        color='darkorange',
        label='Fit',
        linewidth=4)
ax.set_xlim(x.min(), x.max())
ax.set_ylim(0, y.max())
ax.set_xlabel(r'Langwellige Einstrahlung [$W\,m^{-2}$]')
ax.set_ylabel(r'Wasserdampfsäule [$kg\,m^{-2}$]')
ax.legend()
cb = fig.colorbar(pcm)
cb.set_label('Anzahl')
fig.savefig('plots/iwv_lwr_fit.pdf')

# Use the fit...
pyr = clb.csv.read('data/MASTER.txt')
rad = clb.csv.read('data/RAD.txt')

lwr = pyr['L']
lwr_mean = np.array([np.mean(x) for x in np.split(lwr, lwr.size/10)])

iwv_rad = np.ma.masked_invalid(rad['RAD_IWV'])
iwv_pyr = np.ma.masked_invalid(IWV(lwr_mean, *popt))

# Fit vs. measurements
x = np.linspace(300, 420, 100)
fig, ax = plt.subplots()
ax.plot(lwr_mean, iwv_rad, linestyle='none', marker='.', label='Messung')
ax.plot(x, IWV(x, *popt), linestyle='--', linewidth=2, label='Fit', color='k')
ax.set_ylabel('Wasserdampfsäule [$kgm^{-2}$]')
ax.set_xlabel('Langwellige Einstrahlung [$Wm{-2}$]')
ax.set_ylim(0, 40)
ax.legend()
fig.savefig('plots/messung_fit.pdf')

# Timeseries
fig, ax = plt.subplots()
clb.plots.plot_time_series(rad['MPLTIME'], iwv_rad,
                           ylabel='Wasserdampfsäule [$kg\,m^{-2}$]',
                           label='Radiometer',
                           color='darkblue')
clb.plots.plot_time_series(rad['MPLTIME'], iwv_pyr,
                           ylabel='Wasserdampfsäule [$kg\,m^{-2}$]',
                           label='Pyrgeometer',
                           color='darkred')
ax.legend()
ax.set_ylim(0, 40)
fig.savefig('plots/iwv_timeseries.pdf')

# Correlation between fit and measurement.
fig, ax = plt.subplots()
x = y = np.linspace(0, 40, 25)
ax.plot(x, y, linestyle='--', color='k', linewidth=1)
N, x, y = np.histogram2d(iwv_rad, iwv_pyr, (x, y))
pcm = ax.pcolormesh(x, y, N, cmap='Greys')
ax.set_ylabel('Pyrgeometer IWV [$kg\,m^{-2}$]')
ax.set_xlabel('Radiometer IWV [$kg\,m{-2}$]')
ax.set_aspect('equal')
ax.set_title('r = {:.3f}'.format(np.ma.corrcoef(iwv_rad, iwv_pyr)[0, 1]))
fig.colorbar(pcm, label='Anzahl')
fig.savefig('plots/iwv_fit_correlation.pdf')
