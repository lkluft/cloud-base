# -*- coding: utf-8 -*-
"""Estimate the cloud basis height using measurements of longwave radtion.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.constants

def create_dummy_data(LWR=350, N=500, noise=False):
    """Create a dumm array representing LWR data."""
    lwr = LWR * np.ones(N)

    if noise:
        lwr += np.random.randn(N)

    return lwr


def find_value(z, data, T):
    """Return height z[n] where data[n] is closest to T."""
    return z[np.abs(data-T).argmin()]


def lwr_to_temperature(lwr):
    """Calculate the temperature corresponding to an LWR value."""
    return (lwr / sp.constants.Stefan_Boltzmann)**0.25


def plot_lwr(date, lwr, **kwargs):
    """Create a basic timeseries plot of LWR data."""
    fig, ax = plt.subplots()
    ax.plot(date, lwr)
    ax.set_xlabel('date')
    ax.set_ylabel('incoming long-wave radiation [W/m**2]')
    ax.grid('on')

    return fig, ax


def standard_atmosphere(z=np.linspace(0, 86000, 100)):
    """Return international standard atmosphere at given heights."""

    T = -86.28 * np.ones(z.size)
    T[z <= 86000] = -58.5 - 0.0020 * (z[z <= 86000] - z[z < 71802].max())
    T[z <= 71802] = -02.5 - 0.0028 * (z[z <= 71802] - z[z < 51413].max())
    T[z <= 51413] = -02.5
    T[z <= 47350] = -44.5 + 0.0028 * (z[z <= 47350] - z[z < 32162].max())
    T[z <= 32162] = -56.5 + 0.0010 * (z[z <= 32162] - z[z < 20063].max())
    T[z <= 20063] = -56.5
    T[z <= 11019] = 19.00 - 0.0065 * z[z <= 11019]

    return T + 273.15


def main():
    """Main function."""
    lwr = create_dummy_data(LWR=350, noise=True)
    T = lwr_to_temperature(lwr)
    z = np.linspace(0, 20000, 500)
    h = np.array([find_value(z, standard_atmosphere(z), t) for t in T])
    print(h)


if __name__ == '__main__':
    main()
