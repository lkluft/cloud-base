# -*- coding: utf-8 -*-
"""Collection of function to plot basic atmospheric properties.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import typhon.cm


__all__ = ['plot_lwr',
           'plot_ceilo',
           ]


def plot_time_series(date, data, xlabel, ylabel, figsize=(20, 6), **kwargs):
    """Create a basic timeseries plot."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(date, data, **kwargs)
    formatter = mpl.dates.DateFormatter('%d.%m.')
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim(date.min(), date.max())
    ax.set_xticks(np.arange(np.floor(date.min()), np.ceil(date.max())))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid('on')

    return fig, ax


def plot_lwr(date, lwr, **kwargs):
    """Plot LWR time series."""
    xlabel = 'Datum'
    ylabel = 'Langewellige Rückstrahlung [W/m**2]'

    fig, ax = plot_time_series(date, lwr, xlabel, ylabel, **kwargs)

    return fig, ax


def plot_brightness_t(date, T_b, **kwargs):
    """Plot brightness temperature time series."""
    xlabel = 'Datum'
    ylabel = 'Helligkeitstemperatur [K]'
    color = 'DarkRed'

    fig, ax = plot_time_series(date, T_b, xlabel, ylabel, color=color, **kwargs)

    return fig, ax


def plot_ceilo(date, z, back_scat):
    """Create a basic timeseries plot of ceilometer scattering profiles."""
    fig, ax = plt.subplots(figsize=(20, 6.1))
    pcm = ax.pcolormesh(date, z, back_scat,
                        cmap=plt.get_cmap('density', lut=10),
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


def plot_t_profile(date, z, T):
    """Create a basic timeseries plot of ceilometer scattering profiles."""
    fig, ax = plt.subplots(figsize=(20, 6.1))
    pcm = ax.pcolormesh(date, z, T,
                        cmap=plt.get_cmap('temperature', lut=10),
                        # vmin=0,
                        # vmax=1921,
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
    cb.set_label('Temperatur [K]')

    return fig, ax
