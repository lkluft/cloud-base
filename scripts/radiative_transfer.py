# -*- coding: utf-8 -*-
"""Visualise radiative transfer results.
"""
from os.path import join

import numpy as np
import matplotlib.pyplot as plt
import typhon.cm
import typhon.physics
from typhon.arts import xml

import clb


fascod = ['tropical',
          'midlatitude-summer',
          'midlatitude-winter',
          'subarctic-winter',
          ]

for atmosphere in fascod:
    pathto = join('..', 'arts', 'results',  atmosphere, '{}').format

    f = xml.load(pathto('f_grid.xml'))
    z = xml.load(pathto('z_field.xml')).flatten()
    T_s = xml.load(pathto('t_field.xml')).flatten()[0]
    iy = xml.load(pathto('iy.xml')).flatten()
    iy_aux = xml.load(pathto('iy_aux.xml'))
    abs_species = xml.load(pathto('abs_species.xml'))

    abs_sum = iy_aux[1][:, 0, 0, :].T

    # Calculations
    # maximal detection height based on clear-sky ARTS run.
    lwr = clb.integrate_spectrum(f, iy)

    max_height = float(clb.estimate_cloud_height(lwr, T_s))
    print('Maximal detection height for {}: {:.0f}m'.format(atmosphere,
                                                            max_height))

    # opacity for each absorber
    abs_species = [tag[0].split('-')[0] for tag in abs_species]

    def calculate_optical_depth(abs_coeff, height):
        layer_thickness = np.diff(z)
        abs_layer_mean = (abs_coeff[:, 1:] + abs_coeff[:, :-1]) / 2
        opacity = np.sum(layer_thickness * abs_layer_mean, axis=1)
        return opacity

    opacity = {}
    for species, coeff in zip(abs_species, iy_aux[2:]):
        opacity[species] = calculate_optical_depth(coeff[:, 0, 0, ::-1], z)

    # Plots
    f *= 1e-12  # convert to THz
    plt.style.use('typhon')

    # opacity for different species
    fig, ax = plt.subplots()
    for species in abs_species:
        ax.plot(f, opacity[species], label=species)
    ax.set_yscale('log')
    ax.grid('on')
    ax.set_yticks([1e-6, 1e-3, 1, 1e3, 1e6])
    ax.set_xlim(f.min(), f.max())
    ax.set_ylim(1e-6, 10e7)
    ax.set_xlabel('Frequenz [THz]')
    ax.set_ylabel('Optische Dicke')
    ax.legend(ncol=2, fontsize='smaller')

    # opacity in different heights
    dz = np.diff(z)
    abs_mean = (abs_sum[1:, :]+abs_sum[:-1, :]) / 2
    z_mean = (z[1:]+z[:-1]) / 2
    transmission = np.cumsum(abs_mean.T * dz, axis=1).T

    fig1, ax1 = plt.subplots()
    pcm = ax1.pcolormesh(f, z_mean, transmission,
                         vmin=0,
                         vmax=1,
                         cmap=plt.get_cmap('density', lut=10),
                         rasterized=True)
    ax1.set_xlim(f.min(), f.max())
    ax1.set_xlabel('Frequenz [THz]')
    ax1.set_ylim(z_mean.min(), 8000)
    ax1.set_ylabel('Höhe [m]')
    cb = fig1.colorbar(pcm)
    cb.set_label('Optische Dicke')

    # radiance spectrum
    fig2, ax2 = plt.subplots()
    ax2.fill_between(f, typhon.physics.planck(f*1e12, T_s),
                     color='lightgrey',
                     label='Planck')
    ax2.fill_between(f, iy, color='darkred', label='Messung')
    ax2.legend()
    ax2.set_xlim(f.min(), f.max())
    ax2.set_xlabel('Frequenz [THz]')
    ax2.set_ylabel(r'Radianz [$W\,m^{-2}\,sr^{-1}\,Hz^{-1}$]')

    fig.savefig(join('plots', atmosphere + '_opacity.pdf'))
    fig1.savefig(join('plots', atmosphere + '_window.pdf'))
    fig2.savefig(join('plots', atmosphere + '_spectrum.pdf'))
