# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='clb',
    author='Lukas Kluft',
    author_email='lukas.kluft@gmail.com',
    url='https://github.com/lkluft/cloud-base',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    install_requires=[
        'matplotlib>=1.5.1',
        'numpy>=1.10.4',
        'scipy>=0.17.1',
        'typhon>=0.3.0',
    ],
)
