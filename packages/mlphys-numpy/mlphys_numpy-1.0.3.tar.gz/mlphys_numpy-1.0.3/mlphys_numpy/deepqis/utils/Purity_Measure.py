"""
author: Sanjaya Lohani
email: slohani@mlphys_numpy.com
Licence: Apache-2.0
"""
import numpy as np

__author__ = 'Sanjaya Lohani'
__email__ = 'slohani@mlphys_numpy.com'
__licence__ = 'Apache 2.0'
__website__ = "sanjayalohani.com"

def purity(dm_value):
    dm = dm_value.reshape(-1, dm_value.shape[1], dm_value.shape[1])
    mul = np.real(np.trace(np.matmul(dm, np.conjugate(np.transpose(dm, [0, 2, 1]))), axis1=1, axis2=2))
    return mul
