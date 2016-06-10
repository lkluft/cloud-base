#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Send ARTS jobs for all FASCOD atmospheres to SLURM.
"""

import os
from subprocess import call


fascod = ['tropical',
          'midlatitude-summer',
          'midlatitude-winter',
          'subarctic-winter',
          ]

for atmosphere in fascod:
    os.environ['ATMOSPHERE'] = atmosphere
    call(['sbatch', 'arts.job'])
