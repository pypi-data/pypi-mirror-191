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
    sqrt_rho_pred = scipy.linalg.sqrtm(rhos_mat_pred)
    products = np.matmul(np.matmul(sqrt_rho_pred, rhos_true_value), sqrt_rho_pred)
    fidelity = np.trace(np.real(scipy.linalg.sqrtm(products))) ** 2
    return fidelity


def Fidelity_Metric(rhos_mat_pred_batch, rhos_true_value_batch):
    d = rhos_mat_pred_batch.shape[1]
    rhos_mat_pred_batch = np.array(rhos_mat_pred_batch).reshape(-1, d, d)
    rhos_true_value_batch = np.array(rhos_true_value_batch).reshape(-1, d, d)
    fidelity_batch = list(map(evaluate, rhos_mat_pred_batch, rhos_true_value_batch))
    fid_mean = np.array(fidelity_batch).mean()
    return np.array(fidelity_batch), fid_mean

