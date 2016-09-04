# -*- coding: utf-8 -*-
"""Physical functions.
"""
import numpy as np
import typhon.physics
from scipy import constants


__all__ = ['irradiance',
           'irradiance2temperature',
           ]


def irradiance(f, T, solid_angle=np.pi):
    """Integrate the Planck function over the whole hemisphere.

    Parameters:
        f (np.array): Frequency range.
        T (np.array): Temperature.
        solid_angle (float): Solid angle to integrate.
            Default is Pi (hemisphere).

    Returns:
        np.array: Irradiance.

    """
    ff, TT = np.meshgrid(f, T)
    B = typhon.physics.planck(ff, TT)

    B_mean = (B[:, 1:] + B[:, :-1]) / 2
    df = np.diff(ff, axis=1)

    return solid_angle * np.sum(B_mean * df, axis=1)


def irradiance2temperature(lwr):
    """Transform irradiance to blackbody temperature.

    Parameters:
        lwr (np.array): Measured LWR radiances.

    Returns:
        np.array: Brightness temperature in Kelvin.

    """
    return (lwr / constants.Stefan_Boltzmann)**0.25
