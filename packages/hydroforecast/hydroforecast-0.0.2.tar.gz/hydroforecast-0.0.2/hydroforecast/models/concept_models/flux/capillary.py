import numpy as np

from .smoother import smooth_threshold_storage_logistic


def capillary_1(p1=None, S1=None, S1_max=None, S2=None, dt=None):
    """
    Capillary rise: based on deficit in higher reservoir
    Constraints:  f <= S2/dt
    :param p1: maximum capillary rise rate  [mm/d]
    :param S1: current storage in receiving store [mm]
    :param S1_max: maximum storage in receiving store [mm]
    :param S2: current storage in providing store [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.multiply(p1, (1 - S1 / S1_max)), S2 / dt)
    return out


def capillary_2(p1=None, S=None, dt=None):
    """
    Capillary rise at constant rate
    Constraints:  f <= S/dt
    :param p1: base capillary rise rate [mm/d]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(p1, S / dt)
    return out


def capillary_3(p1=None, p2=None, S1=None, S2=None, dt=None):
    """
    Capillary rise scaled by receiving store's deficit up to a storage threshold
    Constraints:  f <= S2
    :param p1: base capillary rise rate [mm/d]
    :param p2: threshold above which no capillary flow occurs [mm]
    :param S1: current storage in receiving store [mm]
    :param S2: current storage in supplying store [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(S2 / dt, p1 * (1 - S1 / p2) * smooth_threshold_storage_logistic(S1, p2))
    return out