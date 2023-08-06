import numpy as np

from .smoother import smooth_threshold_temperature_logistic


def rainfall_1(In=None, T=None, p1=None, varargin=None):
    """
    Rainfall based on temperature threshold
    :param In: incoming precipitation flux [mm/d]
    :param T: current temperature [oC]
    :param p1: temperature threshold above which rainfall occurs [oC]
    :param varargin: smoothing variable r (default 0.01)
    :return:
    """
    out = np.multiply(In, (1 - smooth_threshold_temperature_logistic(T, p1, **varargin)))
    return out


def rainfall_2(In=None, T=None, p1=None, p2=None):
    """
    Rainfall based on a temperature threshold interval
    :param In: incoming precipitation flux [mm/d]
    :param T: current temperature [oC]
    :param p1: midpoint of the combined rain/snow interval [oC]
    :param p2: length of the mixed snow/rain interval [oC]
    :return:
    """
    out = np.amin(In, np.amax(0, np.multiply(In, (T - (p1 - 0.5 * p2))) / p2))
    return out