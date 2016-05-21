# -*- coding: utf-8 -*-
"""Collection of functions to plot basic atmospheric properties.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import typhon.cm


__all__ = ['set_date_axis',
           'plot_time_series',
           'plot_clb',
           'plot_lwr',
           'plot_T_b',
           'plot_back_scat',
           ]


def set_date_axis(ax=None, dateformat='%d.%m.'):
    """Set DateFormatter for given AxesSubplot."""
    formatter = mpl.dates.DateFormatter(dateformat)
    ax.xaxis.set_major_formatter(formatter)
    ax.grid('on', which='both', linestyle='-')


def plot_time_series(date, data, ylabel, ax=None, **kwargs):
    """Create a basic timeseries plot.

    Parameters:
        date (np.array): Dates in matplotlib format.
        data (np.array): Data array.
        ylabel (str): y label.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    if ax is None:
        ax = plt.gca()

    line, = ax.plot(date, data, **kwargs)

    set_date_axis(ax)

    ax.set_xlim(date.min(), date.max())
    ax.set_xticks(np.arange(np.floor(date.min()), np.ceil(date.max())))
    ax.set_xlabel('Datum')
    ax.set_ylabel(ylabel)

    return line


def plot_clb(date, clb, detection_height=2300, ax=None, **kwargs):
    """Plot cloud base height time series.

    Parameters:
        date (np.array): Dates in matplotlib format.
        clb (np.array): Cloud base height.
        detection_height (float): Maximal detection height.
        ax (AxesSubplot): Matplotlib axes.

    """
    ylabel = 'Höhe [m]'

    line = plot_time_series(date, clb,
                            ax=ax,
                            ylabel=ylabel,
                            color='darkorange',
                            alpha=0.7,
                            linewidth=2,
                            label='Wolkenhöhe',
                            **kwargs)

    plot_time_series(date, detection_height * np.ones(date.size),
                     ax=ax,
                     ylabel=ylabel,
                     color='darkred',
                     alpha=0.7,
                     linewidth=2,
                     linestyle='--',
                     label='Max. Detektionshöhe')

    ax.legend()

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
    ylabel = r'Langwellige Rückstrahlung [$W\,m^{-2}$]'

    line = plot_time_series(date, lwr, ylabel, ax=ax, **kwargs)

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
    ylabel = r'$\Delta T_B$ [K]'
    color = 'DarkRed'

    line = plot_time_series(date, T_b, ylabel, ax=ax, color=color, **kwargs)

    return line


def plot_back_scat(date, z, back_scat, ax=None):
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

    ax.set_ylim(0, 4000)
    ax.set_yticks(np.arange(0, 4001, 1000))
    ax.set_yticks(np.arange(0, 4001, 500), minor=True)
    set_date_axis(ax)

    cb = ax.get_figure().colorbar(pcm)
    cb.set_label('Rückstreuintensität')

    return pcm, cb

