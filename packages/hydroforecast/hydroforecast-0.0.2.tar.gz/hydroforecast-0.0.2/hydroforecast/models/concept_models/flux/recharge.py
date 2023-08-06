import numpy as np


def recharge_1(p1=None, S=None, S_max=None, flux=None):
    """
    Recharge as scaled fraction of incoming flux
    :param p1: fraction of flux that is recharge [-]
    :param S: current storage [mm]
    :param S_max: maximum contributing storage [mm]
    :param flux: incoming flux [mm/d]
    :return: 
    """
    out = p1 * S / S_max * flux
    return out


def recharge_2(p1=None, S=None, S_max=None, flux=None):
    """
    Recharge as non-linear scaling of incoming flux
    Constraints:  S >= 0
    :param p1: recharge scaling non-linearity [-]
    :param S: current storage [mm]
    :param S_max: maximum contributing storage [mm]
    :param flux: incoming flux [mm/d]
    :return: 
    """
    out = flux * ((np.amax(S, 0) / S_max) ** p1)
    return out


def recharge_3(p1=None, S=None):
    """
    Linear recharge
    :param p1: time coefficient [d-1]
    :param S: current storage [mm]
    :return:
    """
    out = np.multiply(p1, S)
    return out


def recharge_4(p1=None, S=None, dt=None):
    """
    Constant recharge
    Constraints:  f <= S/dt
    :param p1: time coefficient [d-1]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(p1, S / dt)
    return out


def recharge_5(p1=None, p2=None, S1=None, S2=None):
    """
    Recharge to fulfil evaporation demand if the receiving store is below a threshold
    :param p1: time coefficient [d-1]
    :param p2: storage threshold in S2 [mm]
    :param S1: current storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :return:
    """
    out = np.multiply(np.multiply(p1, S1), (1 - np.amin(1, S2 / p2)))
    return out


def recharge_6(p1=None, p2=None, S=None, dt=None):
    """
    Recharge to fulfil evaporation demand if the receiving store is below a threshold
    Constraints:  f <= S/dt
                  S >= 0      prevents complex numbers
    :param p1: time coefficient [d-1]
    :param p2: non-linear scaling [mm]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.amax(S / dt, 0), np.multiply(p1, np.amax(S, 0) ** p2))
    return out


def recharge_7(p1=None, fin=None):
    """
    Constant recharge limited by incoming flux
    :param p1: maximum recharge rate [mm/d]
    :param fin: incoming flux [mm/d]
    :return:
    """
    out = np.amin(p1, fin)
    return out


def recharge_8(p1=None, S=None, Smax=None, p2=None, dt=None):
    """
    Recharge as non-linear scaling of incoming flux
    Constraints:  f <= S/dt
                  S >= 0
    :param p1: recharge scaling non-linearity [-]
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param p2: maximum flux rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(p2 * ((np.amax(S, 0) / Smax) ** p1), np.amax(S / dt, 0))
    return out