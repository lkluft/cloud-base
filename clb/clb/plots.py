# -*- coding: utf-8 -*-
"""Plot basic atmospheric properties conveniently.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import typhon.cm


__all__ = ['set_date_axis',
           'time_series',
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


def time_series(data, key, ylabel='', ax=None, **kwargs):
    """Create a basic timeseries plot.

    Notes:
        The passed dictionary is expected to store a np.ndarray containing date
        and time information in matplotlib time format. This information has
        to be accessible through the key 'MPLTIME'.

    Parameters:
        data (dict): Dictionary containing time and data.
        key (str): Dictionary key of variable to plot.
            If key is a list of keys, each element in plotted.
        ylabel (str): y label.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    if type(key) is list:
        line = []
        for k in key:
            line.append(time_series(data, k, ylabel=ylabel, ax=ax, **kwargs))
        return line

    if ax is None:
        ax = plt.gca()

    if not 'label' in kwargs:
        kwargs['label'] = key

    date = data['MPLTIME']

    line, = ax.plot(date, data[key], **kwargs)

    set_date_axis(ax)

    ax.set_xlim(date.min(), date.max())
    ax.set_xticks(np.arange(np.floor(date.min()), np.ceil(date.max())))
    ax.set_xlabel('Datum')
    ax.set_ylabel(ylabel)
    ax.legend()

    return line


def plot_clb(data, key='CBH', detection_height=2300, ax=None, **kwargs):
    """Plot cloud base height time series.

    Parameters:
        data (dict): Dictionary containing time and data.
        detection_height (float): Maximal detection height.
        ax (AxesSubplot): Matplotlib axes.

    """
    ylabel = 'Höhe [m]'

    line = time_series(data, key,
                       ax=ax,
                       ylabel=ylabel,
                       color='darkorange',
                       alpha=0.7,
                       linewidth=2,
                       label='Wolkenhöhe',
                       **kwargs)

    data['DETECTION_HEIGHT'] = detection_height * np.ones(data['MPLTIME'].size)
    time_series(data, 'DETECTION_HEIGHT',
                ax=ax,
                ylabel=ylabel,
                color='darkred',
                alpha=0.7,
                linewidth=2,
                linestyle='--',
                label='Max. Detektionshöhe')

    ax.legend()

    return line


def plot_lwr(data, key='L', ax=None, **kwargs):
    """Plot LWR time series.

    Parameters:
        data (dict): Dictionary containing time and data.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    ylabel = r'Langwellige Rückstrahlung [$W\,m^{-2}$]'

    line = time_series(data, key, ylabel, ax=ax, **kwargs)

    return line


def plot_T_b(data, key='L', ax=None, **kwargs):
    """Plot brightness temperature time series.

    Parameters:
        data (dict): Dictionary containing time and data.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    ylabel = r'$\Delta T_B$ [K]'
    color = 'darkred'

    line = time_series(data, key, ylabel, ax=ax, color=color, **kwargs)

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
                        vmax=400,
                        rasterized=True)

    ax.set_ylim(0, 4000)
    ax.set_yticks(np.arange(0, 4001, 1000))
    ax.set_yticks(np.arange(0, 4001, 500), minor=True)
    set_date_axis(ax)

    cb = ax.get_figure().colorbar(pcm)
    cb.set_ticks(np.arange(0, 401, 100))
    cb.set_label('Rückstreuintensität')

    return pcm, cb
