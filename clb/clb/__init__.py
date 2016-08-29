# -*- coding: utf-8 -*-
"""This package provides modules and functions to estimate the
cloud base height (CLB) by measuring the downward longwave radiation.

"""

import matplotlib.pyplot as plt
import numpy as np
import typhon.physics
from scipy.constants import c, h, k, Stefan_Boltzmann

from . import csv
from . import plots


__all__ = ['csv',
           'plots',
           'estimate_cloud_height',
           'integrate_planck',
           'lwr_surrounding',
           'lwr_to_T_b',
           ]


def estimate_cloud_height(lwr, T_s, lapse_rate=-0.0065):
    """Estimate the cloud base height from LWR and 2m temperature.

    Parameters:
        lwr (np.array): LWR.
        T_s (np.array): Near-surface temperature.
        lapse_rate (float): Vertical temperature gradient.

    Returns:
        np.array: Estimated cloud base height.
    """

    return (lwr_to_T_b(lwr) - lwr_to_T_b(lwr_surrounding(T_s))) / lapse_rate


# def planck(f, T):
#     """Planck spectrum for temperature T.

#     Parameters:
#         f (np.array): Frquencies.
#         T (float): Temperature.

#     Returns:
#         np.array: Radiances.

#     """
#     return 2 * h * f**3 / c**2 * (np.exp(h*f/k/T) - 1)**-1


def integrate_planck(f, T):
    """Integrate the Planck function over the whole hemisphere.

    Parameters:
        f (np.array): Frequency grid.
        T (np.array): Temperature grid.

    Returns:
        np.array: Integrated radiances (f x T).

    """
    ff, TT = np.meshgrid(f, T)
    B = typhon.physics.planck(ff, TT)

    B_mean = (B[:, 1:] + B[:, :-1]) / 2
    df = np.diff(ff, axis=1)

    return np.pi * np.sum(B_mean * df, axis=1)


def integrate_spectrum(f, B, factor=np.pi):
    """Integrate a radiance spectrum.

    Parameters:
        f (np.array): Frequencies.
        B (np.array): Radiances.
        factor (float): Integration faktor.
            Default pi for integration over full halfroom.

    Returns:
        float: Power [W * m**-2].

    """
    B_mean = (B[1:] + B[:-1]) / 2
    df = np.diff(f)

    return factor * np.sum(B_mean * df)


def lwr_to_T_b(lwr):
    """Transform LWR radiances into brightness temperatures.

    Parameters:
        lwr (np.array): Measured LWR radiances.

    Returns:
        np.array: Brightness temperature in Kelvin."""

    return (lwr / Stefan_Boltzmann)**0.25


def lwr_surrounding(T):
    """Calculate the integrated radiances for a pyrgeoemter.

    A pyrgeoemter measures the atmospheric infra-red radiation spectrum.
    We assume that it is sensitive to frequencies between 3 THz and 60 THz.

    Parameters:
        T (np.array): Near surface temperature.

    Returns:
        np.array: Integrated radiances for a simplified pyrgeoemter.

        """
    f = np.linspace(3e12, 60e12, 1000)

    return integrate_planck(f, T)
