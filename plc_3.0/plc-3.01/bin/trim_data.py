#!/usr/bin/env python

import numpy as np

a = np.loadtxt('base_2018_plik_TT_cl.dat')
keep = a[:,1:]
print(keep)
np.savetxt('trim.dat', keep)