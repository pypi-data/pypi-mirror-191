"""
author: Sanjaya Lohani
email: slohani@mlphys_numpy.com
Licence: Apache-2.0
"""
import scipy

__author__ = 'Sanjaya Lohani'
__email__ = 'slohani@mlphys_numpy.com'
__licence__ = 'Apache 2.0'
__website__ = "sanjayalohani.com"

def rank(dm_tesnor):
    ranks = np.linalg.matrix_rank(dm_tesnor, tol=1e-5)
    return ranks
