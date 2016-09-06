# -*- coding: utf-8 -*-
"""Mathematical functions.
"""
import numpy as np


__all__ = ['integrate_spectrum',
           'integrate_angles',
           'moving_average',
           'bootstrap',
           ]


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


def integrate_angles(f, y_los, los, dtheta):
    """Integrate spectrum over frequency and angles.

    Parameters:
        f: Frequency grid [Hz].
        y_los: Concatenated spectra for all angles.
        los: Viewing angles.
        dtheta (float): Angle resolution.

    Retuns:
        Integrated spectrum [W/m**2].

    """
    y_int = np.zeros(f.size)
    for y, a in zip(np.split(y_los, los.size), los):
        y_int += (2 * np.pi * np.sin(np.deg2rad(a))
                  * np.cos(np.deg2rad(a)) * y
                  * np.deg2rad(dtheta))
    return integrate_spectrum(f, y_int, factor=1)


def moving_average(x, y, N, mode='same'):
    """Calculate running mean for given timeseries.

    Parameters:
        x (np.ndarray): x data.
        y (np.ndarray): y data.
        N (int): Window size.
        mode (str): Convolve mode 'valid' or 'same'.

    Returns:
        np.ndarray, np.ndarray: Adjusted x data, Averaged y data.

    """
    if mode == 'valid':
        l, t = N//2, -N//2 + 1
        x = x[l:t]
    elif mode == 'full':
        raise Exception(
            'Mode "full" is not supported to prevent boundary effects.'
            'If you know what you are doing, use numpy.convolve to use'
            'full mode.')

    return x, np.convolve(y, np.ones((N,)) / N, mode=mode)


def bootstrap(x, size=None):
    """Generate a bootstrap of given size from x.

    Note:
        This function is a simple wrapper for np.random.choice

    Parameters:
        a (1-D array-like or int):
            If an ndarray, a random sample is generated from its elements.
            If an int, the random sample is generated as if a was np.arange(n)
        size (int or tuple of ints): Output shape.
            If the given shape is, e.g., ``(m, n, k)``, then
            ``m * n * k`` samples are drawn.  Default is None, in which case a
            single value is returned.

    Returns:
        np.ndarray, shape (size,): The generated random samples.

    """
    return np.random.choice(x, size=size, replace=True)
