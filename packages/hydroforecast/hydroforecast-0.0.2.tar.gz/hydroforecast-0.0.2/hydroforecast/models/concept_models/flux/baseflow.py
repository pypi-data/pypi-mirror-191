import numpy as np

from .smoother import smooth_threshold_storage_logistic


def baseflow_1(p1=None, s=None):
    """
    Outflow from a linear reservoir
    :param p1: time scale parameter [d-1]
    :param s: current storage [mm]
    :return:
    """
    out = np.multiply(p1, s)
    return out


def baseflow_2(s=None, p1=None, p2=None, dt=None):
    """
    Non-linear outflow from a reservoir
    Constraints:  f <= S/dt
                  S >= 0  prevents numerical issues with complex numbers
    :param s: current storage [mm]
    :param p1: time coefficient [d]
    :param p2: exponential scaling parameter [-]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin((1.0 / p1 * np.amax(s, 0)) ** (1.0 / p2), np.amax(s, 0) / dt)
    return out


def baseflow_3(S=None, Smax=None):
    # Flux function
    # ------------------
    # Description:
    # Constraints:  None specified
    # @(Inputs):    S    -
    #               Smax -
    """
    Empirical non-linear outflow from a reservoir
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :return:
    """
    out = Smax ** (- 4) / 4 * (S ** 5)
    return out


def baseflow_4(p1=None, p2=None, S=None):
    """
    Exponential outflow from deficit store
    :param p1: base outflow rate [mm/d]
    :param p2: exponent parameter [mm-1]
    :param S: current storage [mm]
    :return:
    """
    out = p1 * np.exp(- 1 * p2 * S)
    return out


def baseflow_5(p1=None, p2=None, S=None, Smax=None, dt=None):
    """
    Non-linear scaled outflow from a reservoir
    Constraints:  f <= S/dt
    :param p1: base outflow rate [mm/d]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(S / dt, p1 * ((np.amax(S, 0) / Smax) ** p2))
    return out


def baseflow_6(p1=None, p2=None, S=None, dt=None):
    """
    Quadratic outflow from a reservoir if a storage threshold is exceeded
    Constraints:  f <= S/dt
    :param p1: linear scaling parameter [mm-1 d-1]
    :param p2: threshold that must be exceeded for flow to occur [mm]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.multiply(np.amin(S / dt, np.multiply(p1, S ** 2)), (1 - smooth_threshold_storage_logistic(S, p2)))
    return out


def baseflow_7(p1=None, p2=None, S=None, dt=None):
    """
    Non-linear outflow from a reservoir
    Constraints:  f <= S/dt, S >= 0
    :param p1: time coefficient [d-1]
    :param p2: exponential scaling parameter [-]
    :param S:  current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(S / dt, np.multiply(p1, np.amax(0, S) ** p2))
    return out


def baseflow_8(p1=None, p2=None, S=None, Smax=None):
    """
    Exponential scaled outflow from a deficit store
    Constraints:  S <= Smax
    :param p1: base outflow rate [mm/d]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :return:
    """
    out = np.multiply(p1, (np.exp(np.multiply(p2, np.amin(1, np.amax(S, 0) / Smax))) - 1))
    return out


def baseflow_9(p1=None, p2=None, S=None):
    """
    Linear outflow from a reservoir if a storage threshold is exceeded
    :param p1: time coefficient [d-1]
    :param p2: storage threshold for flow generation [mm]
    :param S:  current storage [mm]
    :return:
    """
    out = np.multiply(p1, np.amax(0, S - p2))
    return out
