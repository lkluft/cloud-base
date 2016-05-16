# -*- coding: utf-8 -*-
"""Basic template for a python script using numpy and matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def plot_lwr(date, lwr, **kwargs):
    """Create a basic timeseries plot of LWR data."""
    fig, ax = plt.subplots()
    ax.plot(date, lwr, **kwargs)
    formatter = mpl.dates.DateFormatter('%d.%m.')
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim(date.min(), date.max())
    ax.set_xticks(np.arange(np.floor(date.min()), np.ceil(date.max())))
    ax.set_xlabel('Datum')
    ax.set_ylabel('Langewellige Rückstrahlung [W/m**2]')
    ax.grid('on')

    return fig, ax


def plot_ceilo(date, z, back_scat):
    fig, ax = plt.subplots(figsize=(20, 6.1))
    pcm = ax.pcolormesh(date, z, back_scat,
                        cmap=plt.get_cmap('Blues', lut=10),
                        vmin=0,
                        vmax=1921,
                        rasterized=True)
    ax.set_ylabel('Höhe [m]')
    ax.set_ylim(0, 8000)
    ax.set_yticks(np.arange(0, 8001, 500))
    ax.set_xlabel('Datum')
    ax.set_xlim(date.min(), date.max())
    formatter = mpl.dates.DateFormatter('%d.%m.')
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xticks(np.arange(np.floor(date.min()), np.ceil(date.max())))
    ax.grid('on')
    cb = fig.colorbar(pcm)
    cb.set_label('Rückstreuintensität')

    return fig, ax
