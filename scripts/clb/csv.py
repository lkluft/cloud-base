# -*- coding: utf-8 -*-
"""Collection of functions to load specific CSV files.
"""

from matplotlib.dates import strpdate2num
import numpy as np


__all__ = ['read_ceilo',
           'read_mpl_date',
           'read_master',
           ]


def read_ceilo(filename):
    """Read CLB.txt CSV files.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        np.array, np.array: scattering coefficient, height levels

    """
    z = np.arange(10, 10001, 10)

    with open(filename, 'rb') as f:
        tmp = np.genfromtxt(f, delimiter=';', skip_header=7)
        back_scat = np.ma.masked_invalid(tmp[:, 6:]).T
        back_scat = np.ma.masked_less(back_scat, 0)

    return back_scat, z


def read_mpl_date(filename):
    """Extract date and time information from CSV files.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        np.array: Date as matplotlib time value.

    """
    with open(filename, 'rb') as f:
        date = np.genfromtxt(f,
            delimiter=';',
            skip_header=7,
            dtype=str,
            usecols=(0, 1))
    date = [strpdate2num('%d.%m.%Y %H:%M')(' '.join(d)) for d in date]

    return np.array(date)


def read_master(filename):
    """Read MASTER.txt CSV files.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        np.array: Complete data matrix.

    """
    with open(filename, 'rb') as f:
        data = np.genfromtxt(f,
            delimiter=';',
            skip_header=6,
            names=True,
            comments='$')

    return data
