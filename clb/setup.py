# -*- coding: utf-8 -*-
import sys
from distutils.core import setup
from setuptools import find_packages

major, minor, micro = sys.version_info[0:3]
if not (major == 3 and minor >= 5 and micro >= 1):
    sys.exit('Only support Python version >=3.5.1.\n'
             'Found version is {}'.format(sys.version))

setup(
    name='clb',
    author='Lukas Kluft',
    author_email='lukas.kluft@gmail.com',
    url='https://github.com/lkluft/cloud-base',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.txt').read(),
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Science/Research',
        'Topic :: Atmospheric Science',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    install_requires=[
        'matplotlib>=1.5.1',
        'numpy>=1.10.4',
        'scipy>=0.17.1',
        'typhon>=0.3.0',
    ],
)
