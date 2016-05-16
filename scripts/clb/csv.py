#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic template for a python script using numpy and matplotlib.
"""

import numpy as np


def read_ceilo(filename):
    data = {}
    data['z'] = np.arange(10, 10001, 10)

    with open(filename, 'rb') as f:
        tmp = np.genfromtxt(f, delimiter=';', skip_header=7)
        back_scat = np.ma.masked_invalid(tmp[:, 6:]).T
        back_scat = np.ma.masked_less(back_scat, 0)
        data['back_scat'] = back_scat

    return data


def read_mpl_date(filename):
    from matplotlib.dates import strpdate2num

    with open(filename, 'rb') as f:
        date = np.genfromtxt(f,
            delimiter=';',
            skip_header=7,
            dtype=str,
            usecols=(0, 1))
    date = [strpdate2num('%d.%m.%Y %H:%M')(' '.join(d)) for d in date]

    return np.array(date)


def read_master(filename):
    with open(filename, 'rb') as f:
        data = np.genfromtxt(f,
            delimiter=';',
            skip_header=6,
            names=True,
            comments='$')

    return data
