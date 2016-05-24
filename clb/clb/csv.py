# -*- coding: utf-8 -*-
"""Collection of functions to load specific CSV files.
"""

from matplotlib.dates import strpdate2num
import numpy as np


__all__ = ['read',
           'read_scat',
           ]


def _get_mpl_date(date, time):
    """Convert date and time arrays into matplotlib time format..

    Parameters:
        date (np.array): Array containing date strings.
        time (np.array): Array containing time strings.

    Returns:
        np.array: Matplotlib time values.

    """
    dates = zip(date, time)
    mpl_dates =  [strpdate2num('%d.%m.%Y %H:%M')(' '.join(d)) for d in dates]

    return np.array(mpl_dates)


def _get_names(filename):
    """Get variable names from CSV file."""
    with open(filename, "rb") as f:
        for line in f:
            if line.decode().startswith('$Names='):
                return line.decode().split('=')[1].replace(';', ',').strip()


def _get_dtype(variable):
    """Define dtypes for variables in CSV files."""
    if variable == 'DATE':
        return '<U10'
    elif variable == 'TIME':
        return '<U5'
    else:
        return 'f8'


def read(filename, variables=None):
    """Read CSV files.

    Parameters:
        filename (str): Path to CSV file.
        variables (List[str]): List of variables to extract.
            TIME, DATE and MPLTIME are always extracted.

    Returns:
        dict: Dictionary containing the data arrays.

    """
    names = _get_names(filename)
    dtype = [(n, _get_dtype(n)) for n in names.split(',')]

    # Always read DATE and TIME.
    if variables is not None:
        variables = list(set(variables + ['DATE', 'TIME']))

    with open(filename, 'rb') as f:
        data = np.genfromtxt(f,
            delimiter=';',
            skip_header=7,
            dtype=dtype,
            names=names,
            usecols=variables,
            )

    data_dict = {var: data[var] for var in data.dtype.fields}

    data_dict['MPLTIME'] = _get_mpl_date(data['DATE'], data['TIME'])

    return data_dict


def read_scat(filename):
    """Read CLB.txt CSV files.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        np.array, np.array: scattering coefficient, height levels

    """
    z = np.arange(10, 10001, 10)

    with open(filename, 'rb') as f:
        tmp = np.genfromtxt(f, delimiter=';', skip_header=7,
                usecols=tuple(range(6, 1006)))
        back_scat = np.ma.masked_invalid(tmp).T
        back_scat = np.ma.masked_less(back_scat, 0)

    return back_scat, z
