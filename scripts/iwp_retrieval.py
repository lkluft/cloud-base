# -*- coding: utf-8 -*-

""" Retrieve the integrate water vapor path (IWP) through longwave radiation
measurements.

"""
import clb
import typhon
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typhon.arts import xml, atm_fields_compact_get


atmospheres = xml.load('/home/lukas/arts-xml-data/planets/Earth/ECMWF/IFS/Chevallier_91L/chevallierl91_all_full.xml.gz')
ybatch = xml.load('../arts/results/ybatch.xml')
f = xml.load('../arts/results/f_grid.xml')

iwp = np.zeros(len(atmospheres))
lwr = np.zeros(len(ybatch))
for i in range(len(atmospheres)):
    z, T, q = atm_fields_compact_get(
        ['z', 'T', 'abs_species-H2O'],
        atmospheres[i])
    p = atmospheres[i].grids[1]
    iwp[i] = typhon.atmosphere.iwp(q.ravel(), p, T.ravel(), z.ravel())
    lwr[i] = clb.integrate_spectrum(f, ybatch[i], factor=np.pi)

# IWP and LWR correlation (ARTS simulation)
N, x, y = np.histogram2d(iwp, lwr, (25, 25))

plt.style.use('typhon')

fig, ax = plt.subplots()
pcm = ax.pcolormesh(x, y, N.T,
                    cmap=plt.get_cmap('cubehelix_r'),
                    rasterized=True)
ax.set_title('r = {:.3f}'.format(np.corrcoef(iwp, lwr)[0, 1]))
ax.set_xlim(0, x.max())
ax.set_ylim(y.min(), y.max())
ax.set_ylabel(r'Langwellige Einstrahlung [$Wm^{-2}$]')
ax.set_xlabel('Wasserdampfsäule [$kg\,m^{-2}$]')
cb = fig.colorbar(pcm)
cb.set_label('Anzahl')
fig.savefig('plots/iwp_lwr_correlation.pdf')


# Fit IWP(LWR).
def IWP(dT, a, b, c):
    return a * np.exp(b * dT) + c


popt, pcov = curve_fit(IWP, lwr, iwp, p0=[10, 0.001, 0])

fig, ax = plt.subplots()
N, x, y = np.histogram2d(lwr, iwp, (25, 25))
pcm = ax.pcolormesh(x, y, N.T,
                    cmap=plt.get_cmap('density', 8),
                    rasterized=True)
x = np.linspace(lwr.min(), lwr.max(), 100)
ax.plot(x, IWP(x, *popt),
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
fig.savefig('plots/iwp_lwr_fit.pdf')
