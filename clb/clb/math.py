# -*- coding: utf-8 -*-
"""Mathematical functions.
"""
import numpy as np


__all__ = ['integrate_spectrum',
           'moving_average',
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
