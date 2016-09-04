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
    """Calculate running mean of given timeseries.

    Parameters:
        x (np.ndarray): x data.
        y (np.ndarray): y data.
        N (int): Window size.
        mode (str): Convolve mode 'valid', 'same' or 'full'.

    Returns:
        np.ndarray, np.ndarray: Adjusted x data, Averaged y data.

    """
    #TODO: Get returned x array clear.
    if mode == 'valid':
        x = x[N // 2:-N]
    elif mode == 'full':
        x = np.insert(x, 0, x[0] * np.ones(np.ceil(N / 2)))
        x = np.insert(x, -1, x[-1] * np.ones(np.floor(N / 2)))

    return x, np.convolve(y, np.ones((N,)) / N, mode=mode)
