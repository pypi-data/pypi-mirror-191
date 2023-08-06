import numpy as np

from .smoother import smooth_threshold_storage_logistic


def interflow_1(p1=None, S=None, Smax=None, flux=None):
    """
    Interflow as a scaled fraction of an incoming flux
    :param p1: linear scaling parameter [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param flux: incoming flux [mm/d]
    :return:
    """
    out = p1 * S / Smax * flux
    return out


def interflow_2(p1=None, S=None, p2=None, dt=None):
    """
    Non-linear interflow
    Constraints:  f <= S
                  S >= 0  - this avoids numerical issues with complex numbers
    :param p1: time delay [d-1]
    :param S: current storage [mm]
    :param p2: exponential scaling parameter [-]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(p1 * np.amax(S, 0) ** (1 + p2), np.amax(S / dt, 0))
    return out


def interflow_3(p1=None, p2=None, S=None, dt=None):
    """
    Non-linear interflow (variant)
    Constraints:  f <= S
                  S >= 0  - this avoids numerical issues with complex numbers
    :param p1: time delay [d-1]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(p1 * np.amax(S, 0) ** (p2), np.amax(S / dt, 0))
    return out


def interflow_4(p1=None, p2=None, S=None):
    """
    Combined linear and scaled quadratic interflow
    Constraints:  f <= S
                  S >= 0     - prevents numerical issues with complex numbers

    :return:
    """
    out = np.amin(np.amax(S, 0), p1 * np.amax(S, 0) + p2 * np.amax(S, 0) ** 2)
    return out


def interflow_5(p1=None, S=None):
    """
    Linear interflow
    :param p1: time coefficient [d-1]
    :param S: current storage [mm]
    :return:
    """
    out = np.multiply(p1, S)
    return out


def interflow_6(p1=None, p2=None, S1=None, S2=None, S2_max=None):
    """
    Scaled linear interflow if a storage in the receiving store exceeds a threshold
    Constraints:  S2/S2max <= 1
    :param p1: time coefficient [d-1]
    :param p2: threshold as fractional storage in S2 [-]
    :param S1: current storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :param S2_max: maximum storage in S2 [mm]
    :return:
    """
    out = np.multiply(np.multiply(np.multiply(p1, S1), (np.amin(1, S2 / S2_max) - p2)) / (1 - p2),
                      (1 - smooth_threshold_storage_logistic(S2 / S2_max, p2)))
    return out


def interflow_7(S=None, Smax=None, p1=None, p2=None, p3=None, dt=None):
    """
    Non-linear interflow if storage exceeds a threshold
    Constraints:  f <= (S-p1*Smax)/dt
                  S-p1*Smax >= 0  prevents numerical issues with complex numbers
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param p1: storage threshold as fraction of Smax [-]
    :param p2: time coefficient [d]
    :param p3: exponential scaling parameter [-]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.amax(0, (S - np.multiply(p1, Smax)) / dt), (np.amax(0, S - np.multiply(p1, Smax)) / p2) ** (1 / p3))
    return out


def interflow_8(S=None, p1=None, p2=None):
    """
    Linear interflow if storage exceeds a threshold
    Constraints:  f = 0 for S < p2
    :param S: current storage [mm]
    :param p1: time coefficient [d-1]
    :param p2: storage threshold before flow occurs [mm]
    :return:
    """
    out = np.amax(0, p1 * (S - p2))
    return out


def interflow_9(S=None, p1=None, p2=None, p3=None, dt=None):
    """
    Non-linear interflow if storage exceeds a threshold
    Constraints:  f <= S-p2
                  S-p2 >= 0     prevents numerical issues with complex numbers
    :param S: current storage [mm]
    :param p1: time coefficient [d-1]
    :param p2: storage threshold for flow generation [mm]
    :param p3: exponential scaling parameter [-]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.amax((S - p2) / dt, 0), (np.multiply(p1, np.amax(S - p2, 0))) ** p3)
    return out


def interflow_10(S=None, p1=None, p2=None, p3=None):
    """
    Scaled linear interflow if storage exceeds a threshold
    Constraints:  f = 0, for S < p2
    :param S: current storage [mm]
    :param p1: time coefficient [d-1]
    :param p2: threshold for flow generation [mm]
    :param p3: linear scaling parameter [-]
    :return:
    """
    out = p1 * np.amax(0, S - p2) / (p3)
    return out


def interflow_11(p1=None, p2=None, S=None, dt=None, varargin=None):
    """
    Constant interflow if storage exceeds a threshold
    Constraints:  f <= (S-p2_/dt
    :param p1: interflow rate [mm/d]
    :param p2: storage threshold for flow generation [mm]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :param varargin: smoothing variable r (default 0.01), e (default 5.00)
    :return:
    """
    out = np.multiply(np.amin(p1, (S - p2) / dt), (1 - smooth_threshold_storage_logistic(S, p2, **varargin)))
    return out


def interflow_12(p1=None, p2=None, p3=None, S=None, S_max=None, dt=None):
    """
    Non-linear interflow (variant) when current storage is over a threshhold (FC) and zero otherwise
    Constraints:  f <= S-FC
                  S >= 0  - this avoids numerical issues with complex numbers
                  p2*Smax = FC
    :param p1: time delay [d-1]
    :param p2: field capacity coefficient[-]
    :param p3: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param S_max: maximum storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.multiply((S > (p2 * S_max)), (np.amin(p1 * np.amax((S - (p2 * S_max)), 0) ** (p3), np.amax(S / dt, 0))))
    return out