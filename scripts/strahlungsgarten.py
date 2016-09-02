# -*- coding: utf-8 -*-
#
# Copyright © 2016 Lukas Kluft <lukas.kluft@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
import numpy as np
import matplotlib.pyplot as plt
from clb import csv, plots

data = csv.read('data/MASTER.txt')

variable_keys = ['G', 'R', 'L', 'E']

plt.style.use('typhon')
fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(10, 6.1))

kwargs = {
    'G': {'label': r'Kurz $\downarrow$',
          'color': 'darkblue',
          'linestyle': 'solid',
          'ax': ax1,
          },
    'R': {'label': r'Kurz $\uparrow$',
          'color': 'lightblue',
          'linestyle': 'dashed',
          'ax': ax1,
          },
    'L': {'label': r'Lang $\downarrow$',
          'color': 'darkred',
          'linestyle': 'solid',
          'ax': ax2,
          },
    'E': {'label': r'Lang $\uparrow$',
          'color': 'red',
          'linestyle': 'dashed',
          'ax': ax2,
          }
}

for key in variable_keys:
    plots.plot_time_series(data['MPLTIME'], data[key],
                           ylabel=r'$W\,m^{-2}$',
                           linewidth=2,
                           **kwargs[key]
                           )

for ax in [ax1, ax2]:
    ax.legend(ncol=2, fontsize='small')

fig.tight_layout()
fig.savefig('plots/strahlungsgarten.pdf')
