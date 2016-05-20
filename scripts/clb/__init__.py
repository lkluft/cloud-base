# -*- coding: utf-8 -*-
"""This package provides modules and functions to estimate the
cloud level base (CLB) by measuring the downward longwave radiation.

"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import c, h, k, Stefan_Boltzmann

from . import csv
from . import plots


__all__ = ['csv',
           'plots',
           'create_dummy_data',
           'estimate_cloud_height',
           'integrate_planck',
           'lapse_rate',
           'lwr_surrounding',
           'lwr_to_T_b',
           'planck',
           'standard_atmosphere',
           ]


def create_dummy_data(LWR=350, N=500, noise=False):
    """Create a dumm array representing LWR data."""
    lwr = LWR * np.ones(N)

    if noise:
        lwr += np.random.randn(N)

    return lwr


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


def planck(f, T):
    """Planck spectrum for temperature T.

    Parameters:
        f (np.array): Frquencies.
        T (float): Temperature.

    Returns:
        np.array: Radiances.

    """
    return 2 * h * f**3 / c**2 * (np.exp(h*f/k/T) -1)**-1


def integrate_planck(f, T):
    """Integrate the Planck function over the whole hemisphere.

    Parameters:
        f (np.array): Frequency grid.
        T (np.array): Temperature grid.

    Returns:
        np.array: Integrated radiances (f x T).

    """
    ff, TT = np.meshgrid(f, T)
    B = planck(ff, TT)

    # TODO: Use integrate_spectrum in the future.
    return np.pi * np.sum(B * (f[1]-f[0]), axis=1)


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


def lapse_rate(T_s, z, lapse_rate=-0.0065):
    """Generate a time series of temperature profiles.

    This functions takes a time series of surface temperatures and returns an
    first order temperature profile for each time step. For this purpose a
    temperature lapse rate as well as height levels have to be specified.

    Parameters:
        T_s (np.array): Surface temperatures.
        z (np.array): Height levels.
        lapse_rate (float): Lapse rate.

    Returns:
        np.array: Atmospheric temperature profile (T_s x z).

    """
    tt, zz = np.meshgrid(T_s, z)
    return tt + lapse_rate * zz


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


def standard_atmosphere(z=np.linspace(0, 86000, 100), T_s=19., unit='K'):
    """International standard atmosphere temperature at given heights.

    Parameters:
        z (np.array): Array of level heights in m.
        T_s (float): Surface temperature.
        unit (str): Temperature unit 'K' (default) or 'C'.

    Returns:
        np.array: Temperatures at given height levels.

    """

    # https://en.wikipedia.org/wiki/International_Standard_Atmosphere
    T = -86.28 * np.ones(z.size)
    T[z < 86000] = -58.5 - 0.0020 * (z[z < 86000] - z[z <= 71802].max())
    T[z < 71802] = -02.5 - 0.0028 * (z[z < 71802] - z[z <= 51413].max())
    T[z < 51413] = -02.5
    T[z < 47350] = -44.5 + 0.0028 * (z[z < 47350] - z[z <= 32162].max())
    T[z < 32162] = -56.5 + 0.0010 * (z[z < 32162] - z[z <= 20063].max())
    T[z < 20063] = -56.5
    T[z < 11019] = 19.00 - 0.0065 * z[z < 11019]

    # adjust surface temperature
    T = T + (T_s - 19.)

    if unit == 'K':
        T += 273.15
    elif unit != 'C':
        raise Exception("Unknown unit. Allowd units are 'K' and 'C'.")

    return T
