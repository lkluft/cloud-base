# -*- coding: utf-8 -*-
"""Retrieve the integrate water vapor path (IWP)
through longwave radiation measurements.
"""
import clb
import typhon
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typhon.arts import xml, atm_fields_compact_get
from typhon.plots import styles


atmospheres = xml.load('data/chevallierl91_all_q.xml')
ybatch = xml.load('../arts/results/angles/ybatch.xml')
f = xml.load('../arts/results/angles/f_grid.xml')
los = xml.load('../arts/results/angles/sensor_los.xml')


#iwv = np.zeros(len(atmospheres))
#t_s = np.zeros(len(atmospheres))
#lwr = np.zeros(len(ybatch))

iwv = []
t_s = []
lwr = []

for i in range(len(atmospheres)):
    z, T, q = atm_fields_compact_get(
        ['z', 'T', 'abs_species-H2O'],
        atmospheres[i])
    p = atmospheres[i].grids[1]
#    iwv[i] = typhon.atmosphere.iwv(q.ravel(), p, T.ravel(), z.ravel())
#    t_s[i] = T[0]
#    lwr[i] = clb.math.integrate_angles(f, ybatch[i], los, dtheta=15)
    if T[0] > 283.15 and p[0] > 95000:
        iwv.append(typhon.atmosphere.iwv(q.ravel(), p, T.ravel(), z.ravel()))
        t_s.append(float(T[0]))
        lwr.append(clb.math.integrate_angles(f, ybatch[i], los, dtheta=15))

iwv = np.array(iwv)
t_s = np.array(t_s)
lwr = np.array(lwr)

# IWP and LWR correlation (ARTS simulation)
N, x, y = np.histogram2d(iwv, lwr, (25, 25))

plt.style.use(styles('typhon'))

fig, ax = plt.subplots()
pcm = ax.pcolormesh(x, y, N.T,
                    cmap=plt.get_cmap('cubehelix_r', 8),
                    rasterized=True)
# ax.set_title('r = {:.3f}'.format(np.corrcoef(iwv, lwr)[0, 1]))
ax.set_xlim(0, x.max())
ax.set_ylim(y.min(), y.max())
ax.set_ylabel(r'Langwellige Einstrahlung [$Wm^{-2}$]')
ax.set_xlabel('Wasserdampfsäule [$kg\,m^{-2}$]')
cb = fig.colorbar(pcm)
cb.set_label('Anzahl')
fig.savefig('plots/iwv_lwr_correlation.pdf')


# Fit IWV(LWR).
def IWV(x, a, b, c):
    lwr, t = x
    return a * np.exp(b * lwr) + c #* t + d


popt, pcov = curve_fit(IWV, (lwr, t_s), iwv, p0=[10, 0.001, 0])
header = ('IWV(x, a, b, c) = a * np.exp(b * x[0]) + c\n'
          'a;b;c')
np.savetxt('data/coefficients.txt', popt, header=header, delimiter=';')

fig, ax = plt.subplots()
N, x, y = np.histogram2d(lwr, iwv, (25, 25))
pcm = ax.pcolormesh(x, y, N.T,
                    cmap=plt.get_cmap('density', 8),
                    rasterized=True)
x = (np.linspace(lwr.min(), lwr.max(), 100), 303.15)
ax.plot(x[0], IWV(x, *popt),
        color='darkorange',
        label='Fit',
        linewidth=4)
ax.set_xlim(x[0].min(), x[0].max())
ax.set_ylim(0, y.max())
ax.set_xlabel(r'Langwellige Einstrahlung [$W\,m^{-2}$]')
ax.set_ylabel(r'Wasserdampfsäule [$kg\,m^{-2}$]')
ax.legend()
cb = fig.colorbar(pcm)
cb.set_label('Anzahl')
fig.savefig('plots/iwv_lwr_fit.pdf')

# Use the fit...
pyr = clb.csv.read('data/35/MASTER.txt')
rad = clb.csv.read('data/35/RAD.txt')

mean = {}
for var in ['L', 'TT002']:
    mean['MPLTIME'], mean[var] = clb.math.block_average(
                                    pyr['MPLTIME'],
                                    pyr[var],
                                    10)

iwv_rad = np.ma.masked_invalid(rad['RAD_IWV'])
iwv_rad = np.ma.masked_greater(iwv_rad, 50)
x = (mean['L'], mean['TT002'] + 273.15)
#x = mean['L']
iwv_pyr = np.ma.masked_invalid(IWV(x, *popt))
_, iwv_pyr = clb.math.moving_average(np.ones(iwv_pyr.size), iwv_pyr, 18)
offset = np.nanmean(iwv_pyr - iwv_rad)

# Fit vs. measurements
x = (np.linspace(300, 420, 100), 293.15)
fig, ax = plt.subplots()
ax.plot(mean['L'], iwv_rad, linestyle='none', marker='.', label='Messung')
ax.plot(x[0], IWV(x, *popt), linestyle='--', linewidth=2, label='Fit', color='k')
ax.set_ylabel('Wasserdampfsäule [$kgm^{-2}$]')
ax.set_xlabel('Langwellige Einstrahlung [$Wm{-2}$]')
ax.set_ylim(0, 40)
ax.legend()
fig.savefig('plots/messung_fit.pdf')

# Timeseries
data = {
    'DATE': rad['DATE'],
    'TIME': rad['TIME'],
    'MPLTIME': rad['MPLTIME'],
    'RAD_IWV': iwv_rad,
    'PYR_IWV': iwv_pyr,
    'PYR_IWV_corrected': iwv_pyr - offset,
    }

clb.csv.write_dict('data/iwv.txt', data)

fig, ax = plt.subplots(figsize=(20, 8))
clb.plots.time_series(data, 'RAD_IWV',
                      ylabel='Wasserdampfsäule [$kg\,m^{-2}$]',
                      linewidth=4,
                      label='Radiometer',
                      color='darkblue')
clb.plots.time_series(data, 'PYR_IWV',
                      ylabel='Wasserdampfsäule [$kg\,m^{-2}$]',
                      linewidth=4,
                      label='Pyrgeometer',
                      color='darkorange')
ax.legend()
ax.set_ylim(0, 50)
fig.savefig('plots/iwv_timeseries.pdf')
fig.savefig('plots/iwv_timeseries.svg')

fig, ax = plt.subplots()
clb.plots.time_series(data, 'RAD_IWV',
                      ylabel='Wasserdampfsäule [$kg\,m^{-2}$]',
                      label='Radiometer',
                      color='darkblue')
clb.plots.time_series(data, 'PYR_IWV_corrected',
                      ylabel='Wasserdampfsäule [$kg\,m^{-2}$]',
                      label='Pyrgeometer - {:3.1f}'.format(offset),
                      color='darkorange')
ax.legend()
ax.set_ylim(0, 50)
fig.savefig('plots/iwv_timeseries_corrected.pdf')

# Correlation between fit and measurement.
st = clb.math.compare_arrays(iwv_rad, iwv_pyr, verbose=True)
st_c = clb.math.compare_arrays(iwv_rad, iwv_pyr - offset, verbose=True)

fig, ax = plt.subplots()
x = y = np.linspace(0, 50, 25)
ax.plot(x, y, linestyle='--', color='k', linewidth=1)
N, x, y = np.histogram2d(iwv_rad, iwv_pyr, (x, y))
pcm = ax.pcolormesh(x, y, N.T, cmap=plt.get_cmap('Greys', 8))
ax.set_ylabel('Pyrgeometer IWV [$kg\,m^{-2}$]')
ax.set_xlabel('Radiometer IWV [$kg\,m^{-2}$]')
ax.set_aspect('equal')
# ax.set_title('r = {:.3f}'.format(st_c.corrcoef))
fig.colorbar(pcm, label='Anzahl')
fig.savefig('plots/iwv_fit_correlation.pdf')
