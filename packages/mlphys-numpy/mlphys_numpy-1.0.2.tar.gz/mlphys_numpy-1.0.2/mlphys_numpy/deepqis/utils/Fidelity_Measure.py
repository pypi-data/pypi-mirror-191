"""
author: Sanjaya Lohani
email: slohani@mlphys_numpy.com
Licence: Apache-2.0
"""
from typing import Any

import scipy
import numpy as np


__author__ = 'Sanjaya Lohani'
__email__ = 'slohani@mlphys_numpy.com'
__licence__ = 'Apache 2.0'
__website__ = "sanjayalohani.com"


def evaluate(rhos_mat_pred, rhos_true_value):
    sqrt_rho_pred = scipy.linalg.sqrtm(rho_mat_pred)
    products = np.matmul(np.matmul(sqrt_rho_pred, rhos_true_value), sqrt_rho_pred)
    fidelity = np.trace(np.real(scipy.linalg.sqrtm(products))) ** 2
    return fidelity


def Fidelity_Metric(rhos_mat_pred_batch, rhos_true_value_batch):
    fidelity_batch = list(map(evaluate, rhos_ture_value_batch, rhos_true_value_batch))
    fid_mean = np.array(fidelity_batch).mean()
    return np.array(fidelity_batch), fid_mean

