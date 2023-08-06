import numpy as np


def depression_1(p1=None, p2=None, S=None, Smax=None, flux=None, dt=None):
    """
    Exponential inflow to surface depression store
    Constraints:  f <= (Smax-S)/dt, S <= Smax
    :param p1: linear scaling parameter [-]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param flux:
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.multiply(np.multiply(p1, np.exp(np.multiply(- 1.0 * p2, S) / np.amax(Smax - S, 0))), flux), np.amax((Smax - S) / dt, 0))
    return out
