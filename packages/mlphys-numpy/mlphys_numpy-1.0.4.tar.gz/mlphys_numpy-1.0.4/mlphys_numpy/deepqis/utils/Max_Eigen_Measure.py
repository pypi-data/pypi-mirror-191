"""
author: Sanjaya Lohani
email: slohani@mlphys_numpy.com
Licence: Apache-2.0
"""
import tensorflow as tf
import numpy as np

__author__ = 'Sanjaya Lohani'
__email__ = 'slohani@mlphys_numpy.com'
__licence__ = 'Apache 2.0'
__website__ = "sanjayalohani.com"

def max_eigen(dm_tensor):
    eigv, _ = np.linalg.eigh(dm_tensor)
    eigv = np.real(eigv)
    eigv_max = np.max(eigv, axis=1)
    return eigv_max


def mean_eigen_order(dm_tensor):
    eigv, _ = np.linalg.eigh(dm_tensor)
    eigv = np.real(eigv)
    eigv_mean = np.mean(np.sort(eigv, axis=1), axis=0)
    return eigv_mean
