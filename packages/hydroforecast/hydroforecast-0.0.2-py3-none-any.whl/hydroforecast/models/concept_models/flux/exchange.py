import numpy as np


def exchange_1(p1=None, p2=None, p3=None, S=None, fmax=None, dt=None):
    """
    Water exchange between aquifer and channel
    Constraints:  f <= fIn
    :param p1: linear scaling parameter [-]
    :param p2: linear scaling parameter [-]
    :param p3: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param fmax: maximum flux size [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(np.multiply((p1 * np.abs(S / dt) + p2 * (1 - np.exp(- 1 * p3 * np.abs(S / dt)))), np.sign(S)), - 1 * fmax)
    return out


def exchange_2(p1=None, S1=None, S1max=None, S2=None, S2max=None):
    """
    Water exchange based on relative storages
    :param p1: base exchange rate [mm/d]
    :param S1: current storage in S1 [mm]
    :param S1max: maximum storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :param S2max: maximum storage in S2 [mm]
    :return:
    """
    out = p1 * (S1 / S1max - S2 / S2max)
    return out


def exchange_3(p1=None, S=None, p2=None):
    """
    Water exchange with infinite size store based on threshold
    :param p1: base leakage time delay [d-1]
    :param S: threshold for flow reversal [mm]
    :param p2: current storage [mm]
    :return:
    """
    out = p1 * (S - p2)
    return out
