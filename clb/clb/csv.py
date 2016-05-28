# -*- coding: utf-8 -*-
"""Load CSV files stored in Wettermast format.
"""
import re

from matplotlib.dates import strpdate2num
import numpy as np


__all__ = ['read',
           'read_scat',
           ]


def _get_mpl_date(dates, fmt='%d.%m.%Y %H:%M'):
    """Convert date strings into matplotlib time format.

    Parameters:
        dates (np.array): Array containing date strings.
        fmt (str): Date string format [0].

    [0] http://pubs.opengroup.org/onlinepubs/009695399/functions/strptime.html

    Returns:
        np.array: Matplotlib time values.

    """
    return np.array([strpdate2num(fmt)(d) for d in dates])


def _get_names(filename):
    """Get variable names from CSV file.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        str: Comma separated list of variable names.
    """
    with open(filename, "rb") as f:
        for line in f:
            if line.decode().startswith('$Names='):
                return line.decode().split('=')[1].replace(';', ',').strip()


def _get_dtype(variable):
    """Define dtypes for variables in CSV files.

    Parameters:
        variable (str): Variable name.

    Returns:
        str: dtype of given variable.
    """
    variable_dtypes = {
            'DATE': '<U10',
            'TIME': '<U5',
            }

    if variable in variable_dtypes:
        dtype = variable_dtypes[variable]
    else:
        dtype = 'f8'

    return dtype


def read(filename, variables=None, output=None):
    """Read CSV files.

    Parameters:
        filename (str): Path to CSV file.
        variables (List[str]): List of variables to extract.
        output (dict): Dictionary that is updated with read data.

    Returns:
        dict: Dictionary containing the data arrays.

    """
    names = _get_names(filename)
    dtype = [(n, _get_dtype(n)) for n in names.split(',')]

    # Read DATE and TIME even if they are not explicitly listed.
    if variables is not None:
        usecols = list(set(variables + ['DATE', 'TIME']))
    else:
        variables = names.split(',')
        usecols = None

    with open(filename, 'rb') as f:
        data = np.genfromtxt(f,
            delimiter=';',
            skip_header=7,
            dtype=dtype,
            names=names,
            usecols=usecols,
            )

    # Convert structured array to dictionary.
    data_dict = {var: data[var] for var in variables}

    # Always convert DATE and TIME into matplotlib time.
    dates = [' '.join(d) for d in zip(data['DATE'], data['TIME'])]
    data_dict['MPLTIME'] = _get_mpl_date(dates)

    if output is not None:
        data_dict = {**output, **data_dict}

    return data_dict


def read_scat(filename, dz=10, scat_name='CLB_B\d{5}', output=None):
    """Read scattering coefficients from CSV file.

    Parameters:
        filename (str): Path to CSV file.
        output (dict): Dictionary that is updated with read data.
        dz (float): Height resolution of the ceilometer.
        scat_name (str): Python regular expression [0] matching
            the variable name of the scattering coefficients.

    [0] https://docs.python.org/3.1/library/re.html

    Returns:
        np.array, np.array: scattering coefficient, height levels

    """

    data_dict = read(filename)

    p = re.compile(scat_name)

    scat_vars = [var for var in data_dict.keys() if p.match(var)]
    scat_vars.sort()

    back_scat = np.vstack([data_dict[v] for v in scat_vars])
    back_scat = np.ma.masked_invalid(back_scat)
    back_scat = np.ma.masked_less(back_scat, 0)

    data_dict['CLB_MATRIX'] = back_scat

    # Extract height level from variable names.
    data_dict['CLB_Z'] = np.arange(dz, dz * (len(scat_vars)+1), dz)

    if output is not None:
        data_dict = {**output, **data_dict}

    return data_dict
