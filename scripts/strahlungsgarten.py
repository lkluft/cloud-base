# -*- coding: utf-8 -*-
"""Plot an overview of shortwave and longwave radiation measurements.
"""
import matplotlib.pyplot as plt
from clb import csv, plots

data = {}
for week in [34, 35, 36]:
    csv.read('data/{}/MASTER.txt'.format(week), output=data)

variable_keys = ['G', 'R', 'L', 'E']

plt.style.use('typhon')
fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(10, 6.1))

kwargs = {
    'G': {'label': r'Kurz $\downarrow$',
          'color': 'blue',
          'linestyle': 'solid',
          'ax': ax1,
          },
    'R': {'label': r'Kurz $\uparrow$',
          'color': 'darkorange',
          'linestyle': 'solid',
          'ax': ax1,
          },
    'L': {'label': r'Lang $\downarrow$',
          'color': 'red',
          'linestyle': 'solid',
          'ax': ax2,
          },
    'E': {'label': r'Lang $\uparrow$',
          'color': 'darkgreen',
          'linestyle': 'solid',
          'ax': ax2,
          }
}

for key in variable_keys:
    plots.time_series(
        data, key,
        ylabel=r'$W\,m^{-2}$',
        linewidth=2,
        **kwargs[key]
        )

for ax in [ax1, ax2]:
    ax.legend(ncol=2, fontsize='small')
ax1.set_ylim(0, 1200)
ax2.set_ylim(300, 520)

fig.tight_layout()
fig.savefig('plots/strahlungsgarten.pdf')
