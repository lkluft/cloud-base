# -*- coding: utf-8 -*-
"""Collection of function to plot basic atmospheric properties.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import typhon.cm


__all__ = ['plot_time_series',
           'plot_lwr',
           'plot_T_b',
           'plot_ceilo',
           ]


def plot_time_series(date, data, xlabel, ylabel, ax=None, **kwargs):
    """Create a basic timeseries plot.

    Parameters:
        date (np.array): Dates in matplotlib format.
        data (np.array): Data array.
        xlabel (str): x label.
        ylabel (str): y label.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    if ax is None:
        ax = plt.gca()

    line, = ax.plot(date, data, **kwargs)
    formatter = mpl.dates.DateFormatter('%d.%m.')
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim(date.min(), date.max())
    ax.set_xticks(np.arange(np.floor(date.min()), np.ceil(date.max())))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid('on')

    return line


def plot_lwr(date, lwr, ax=None, **kwargs):
    """Plot LWR time series.

    Parameters:
        date (np.array): Dates in matplotlib format.
        data (np.array): LWR data array.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    xlabel = 'Datum'
    ylabel = r'Langwellige Rückstrahlung [$W\,m^{-2}$]'

    line = plot_time_series(date, lwr, xlabel, ylabel, ax=ax, **kwargs)

    return line


def plot_T_b(date, T_b, ax=None, **kwargs):
    """Plot brightness temperature time series.

    Parameters:
        date (np.array): Dates in matplotlib format.
        data (np.array): Brightness temperature data array with.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    xlabel = 'Datum'
    ylabel = r'$\Delta T_B$ [K]'
    color = 'DarkRed'

    line = plot_time_series(date, T_b, xlabel, ylabel, ax=ax, color=color,
            **kwargs)

    return line


def plot_ceilo(date, z, back_scat, ax=None):
    """Create a basic timeseries plot of ceilometer scattering profiles.

    Parameters:
        date (np.array): Dates in matplotlib format.
        z (np.array): Height level data array.
        back_scat (np.array): Ceilometer back scattering coefficients.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        QuadMesh, Colorbar

    """
    if ax is None:
        ax = plt.gca()
    pcm = ax.pcolormesh(date, z, back_scat,
                        cmap=plt.get_cmap('density', lut=10),
                        vmin=0,
                        vmax=1921,
                        rasterized=True)
    ax.set_ylabel('Höhe [m]')
    ax.set_ylim(0, 4000)
    ax.set_yticks(np.arange(0, 4001, 1000))
    ax.set_yticks(np.arange(0, 4001, 500), minor=True)
    ax.set_xlabel('Datum')
    ax.set_xlim(date.min(), date.max())
    formatter = mpl.dates.DateFormatter('%d.%m.')
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xticks(np.arange(np.floor(date.min()), np.ceil(date.max())))
    ax.grid('on', which='both', linestyle='-')
    cb = ax.get_figure().colorbar(pcm)
    cb.set_label('Rückstreuintensität')

    return pcm, cb
