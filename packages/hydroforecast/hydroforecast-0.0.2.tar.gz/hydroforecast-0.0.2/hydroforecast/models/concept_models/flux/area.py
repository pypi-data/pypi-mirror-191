import numpy as np

from .smoother import smooth_threshold_storage_logistic


def area_1(p1, p2, s, s_min, s_max, varargin):
    """
    Description:  Auxiliary function that calculates a variable contributing area.
    Constraints:  A <= 1
    :param p1: linear scaling parameter [-]
    :param p2: exponential scaling parameter [-]
    :param s: current storage [mm]
    :param s_min: minimum contributing storage [mm]
    :param s_max: maximum contributing storage [mm]
    :param varargin: smoothing variable r (default 0.01), and e (default 5.00)
    :return:
    """
    out = min(1, p1 * (max(0, s - s_min) / (s_max - s_min)) ^ p2) \
          * (1 - smooth_threshold_storage_logistic(s, s_min, *varargin))
    return out
