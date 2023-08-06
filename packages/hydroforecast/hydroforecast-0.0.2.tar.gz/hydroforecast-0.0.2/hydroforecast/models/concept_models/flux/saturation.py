import numpy as np
import scipy
from .smoother import smooth_threshold_storage_logistic


def saturation_1(In=None, S=None, Smax=None, varargin=None):
    """
    Saturation excess from a store that has reached maximum capacity
    :param In: incoming flux [mm/d]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param varargin:  smoothing variable r (default 0.01), e (default 5.00)
    :return:
    """
    out = np.multiply(In, (1 - smooth_threshold_storage_logistic(S, Smax, **varargin)))
    return out


def saturation_2(S=None, Smax=None, p1=None, In=None):
    """
    Saturation excess from a store with different degrees of saturation
    Constraints:  1-S/Smax >= 0 prevents numerical issues with complex numbers
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param p1: non-linear scaling parameter [-]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply((1 - min(1, max(0, (1 - S / Smax))) ** p1), In)
    return out


def saturation_3(S=None, Smax=None, p1=None, In=None):
    """
    Saturation excess from a store with different degrees of saturation (exponential variant)
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param p1: linear scaling parameter [-]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply((1 - (1 / (1 + np.exp((S / Smax + 0.5) / p1)))), In)
    return out


def saturation_4(S=None, Smax=None, In=None):
    """
    Saturation excess from a store with different degrees of saturation (quadratic variant)
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.amax(0, np.multiply((1 - (S / Smax) ** 2), In))
    return out


def saturation_5(S=None, p1=None, p2=None, In=None):
    """
    Deficit store: exponential saturation excess based on current storage and a threshold parameter
    Constraints:  S >= 0      prevents numerical issues with complex numbers
    :param S: deficit threshold above which no flow occurs [mm]
    :param p1: exponential scaling parameter [-]
    :param p2: current deficit [mm]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply((1 - np.amin(1, (np.amax(S, 0) / p1) ** p2)), In)
    return out


def saturation_6(p1=None, S=None, Smax=None, In=None):
    """
    Saturation excess from a store with different degrees of saturation (linear variant)
    :param p1: linear scaling parameter [-]
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = p1 * S / Smax * In
    return out


def saturation_7(p1=None, p2=None, p3=None, p4=None, p5=None, S=None, In=None):
    """
    Saturation excess from a store with different degrees of saturation (gamma function variant)
    Constraints:  f = 0, for x-p3 < 0
                  S >= 0      prevents numerical problems with integration
    :param p1: scaling parameter [-]
    :param p2: gamma function parameter [-]
    :param p3: storage threshold for flow generation [mm]
    :param p4: absolute scaling parameter [mm]
    :param p5: linear scaling parameter [-]
    :param S: current storage [mm]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply(integral(
        lambda x=None: np.multiply(np.multiply(1.0 / (np.multiply(p1, scipy.special.gamma(p2))), (np.amax(x - p3, 0) / p1) ** (p2 - 1)),
                                   np.exp(- 1.0 * np.amax(x - p3, 0) / p1)), np.multiply(p5, np.amax(S, 0)) + p4, Inf), In)
    return out


def saturation_8(p1=None, p2=None, S=None, Smax=None, In=None):
    """
    Saturation excess flow from a store with different degrees of saturation (min-max linear variant)
    :param p1: minimum fraction contributing area [-]
    :param p2: maximum fraction contributing area [-]
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = (p1 + (p2 - p1) * S / Smax) * In
    return out


def saturation_9(In=None, S=None, St=None, varargin=None):
    """
    Deficit store: Saturation excess from a store that has reached maximum capacity
    :param In: incoming flux [mm/d]
    :param S: current storage [mm]
    :param St: threshold for flow generation [mm], 0 for deficit
    :param varargin: smoothing variable r (default 0.01), e (default 5.00)
    :return:
    """
    out = np.multiply(In, smooth_threshold_storage_logistic(S, St, **varargin))
    return out


def saturation_10(p1=None, p2=None, p3=None, S=None, In=None):
    """
    Saturation excess flow from a store with different degrees of saturation (min-max exponential variant)
    :param p1: maximum contributing fraction area [-]
    :param p2: minimum contributing fraction area [-]
    :param p3: exponentia scaling parameter [-]
    :param S: current storage [mm]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply(np.amin(p1, p2 + np.multiply(p2, np.exp(np.multiply(p3, S)))), In)
    return out


def saturation_11(p1=None, p2=None, S=None, Smin=None, Smax=None, In=None, varargin=None):
    """
    Saturation excess flow from a store with different degrees of saturation (min exponential variant)
    Constraints:  f <= In
    :param p1: linear scaling parameter [-]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param Smin: minimum contributing storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param In: incoming flux [mm/d]
    :param varargin: smoothing variable r (default 0.01), e (default 5.00)
    :return:
    """
    out = np.multiply(np.multiply(In, np.amin(1, np.multiply(p1, (np.amax(0, S - Smin) / (Smax - Smin)) ** p2))),
                      (1 - smooth_threshold_storage_logistic(S, Smin)))
    return out


def saturation_12(p1=None, p2=None, In=None):
    """
    Saturation excess flow from a store with different degrees of saturation (min-max linear variant)
    :param p1: maximum contributing fraction area [-]
    :param p2: minimum contributing fraction area [-]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply(np.amax(0, (p1 - p2) / (1 - p2)), In)
    return out


def saturation_13(p1=None, p2=None, S=None, In=None):
    """
    Saturation excess flow from a store with different degrees of saturation (normal distribution variant)
    :param p1: soil depth where 50# of catchment contributes to overland flow [mm]
    :param p2: soil depth where 16# of catchment contributes to overland flow [mm]
    :param S: current storage [mm]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply(In, normcdf(log10(np.amax(0, S) / p1) / log10(p1 / p2)))
    return out


def saturation_14(p1=None, p2=None, S=None, Smax=None, In=None):
    """
    Saturation excess flow from a store with different degrees of saturation (two-part exponential variant)
    :param p1: fraction of area where inflection point is [-]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param In: incoming flux [mm/d]
    :return:
    """
    out = np.multiply((np.multiply((np.multiply((0.5 - p1) ** (1 - p2), np.amax(0, S / Smax) ** p2)), (S / Smax <= 0.5 - p1)) + np.multiply(
        (1 - np.multiply((0.5 + p1) ** (1 - p2), np.amax(0, 1 - S / Smax) ** p2)), (S / Smax > 0.5 - p1))), In)
    return out
