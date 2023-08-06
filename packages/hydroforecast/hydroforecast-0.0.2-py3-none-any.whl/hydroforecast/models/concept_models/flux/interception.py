import numpy as np

from .smoother import smooth_threshold_storage_logistic


def interception_1(In=None, S=None, S_max=None, varargin=None):
    """
    Interception excess when maximum capacity is reached
    :param In: incoming flux [mm/d]
    :param S: current storage [mm]
    :param S_max: maximum storage [mm]
    :param varargin: smoothing variable r (default 0.01), e (default 5.00)
    :return:
    """
    out = np.multiply(In, (1 - smooth_threshold_storage_logistic(S, S_max, varargin(1), varargin(2))))
    return out


def interception_2(In=None, p1=None):
    """
    Interception excess after a constant amount is intercepted
    Constraints:  f >= 0
    :param In: incoming flux [mm/d]
    :param p1: interception and evaporation capacity [mm/d]
    :return:
    """
    out = np.amax(In - p1, 0)
    return out


def interception_3(p1=None, In=None):
    """
    Interception excess after a fraction is intercepted
    :param p1: fraction throughfall [-]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply(p1, In)
    return out


def interception_4(p1=None, p2=None, t=None, t_max=None, In=None, dt=None):
    """
    Interception excess after a time-varying fraction is intercepted
    Constraints:  f >= 0
    :param p1: mean throughfall fraction [-]
    :param p2: timing of maximum throughfall fraction [d]
    :param t: current time step [-]
    :param t_max: duration of the seasonal cycle [d]
    :param In: incoming flux [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(0, p1 + (1 - p1) * np.cos(2 * np.pi * (t * dt - p2) / t_max)) * In
    return out


def interception_5(p1=None, p2=None, In=None):
    """
    Interception excess after a combined absolute amount and fraction are intercepted
    Constraints:  f >= 0
    :param p1: fraction that is not throughfall [-]
    :param p2: constnat interception and evaporation [mm/d]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.amax(np.multiply(p1, In) - p2, 0)
    return out
