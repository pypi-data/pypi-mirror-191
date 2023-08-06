import numpy as np

from .smoother import smooth_threshold_temperature_logistic


def snowfall_1(In=None, T=None, p1=None, varargin=None):
    """
    Snowfall based on temperature threshold
    :param In: incoming precipitation flux [mm/d]
    :param T: current temperature [oC]
    :param p1: temperature threshold below which snowfall occurs [oC]
    :param varargin: smoothing variable r (default 0.01)
    :return:
    """
    out = np.multiply(In, (smooth_threshold_temperature_logistic(T, p1, **varargin)))
    return out


def snowfall_2(In=None, T=None, p1=None, p2=None):
    """
    Snowfall based on a temperature threshold interval
    :param In: incoming precipitation flux [mm/d]
    :param T: current temperature [oC]
    :param p1: midpoint of the combined rain/snow interval [oC]
    :param p2: length of the mixed snow/rain interval [oC]
    :return:
    """
    out = np.amin(In, np.amax(0, np.multiply(In, (p1 + 0.5 * p2 - T)) / p2))
    return out
