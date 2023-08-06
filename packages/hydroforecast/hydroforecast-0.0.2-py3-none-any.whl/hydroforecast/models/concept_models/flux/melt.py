import numpy as np

from .smoother import smooth_threshold_storage_logistic


def melt_1(p1=None, p2=None, T=None, S=None, dt=None):
    """
    Snowmelt from degree-day-factor
    Constraints:  f <= S/dt
    :param p1: degree-day factor [mm/oC/d]
    :param p2: temperature threshold for snowmelt [oC]
    :param T: current temperature [oC]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(np.amin(p1 * (T - p2), S / dt), 0)
    return out


def melt_2(p1=None, S=None, dt=None):
    """
    Snowmelt at a constant rate
    Constraints:  f <= S/dt
    :param p1: melt rate [mm/d]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(p1, S / dt)
    return out


def melt_3(p1=None, p2=None, T=None, S1=None, S2=None, St=None, dt=None, varargin=None):
    """
    Glacier melt provided no snow is stored on the ice layer
    Constraints:  f <= S1/dt
    :param p1: degree-day factor [mm/oC/d]
    :param p2: temperature threshold for snowmelt [oC]
    :param T: current temperature [oC]
    :param S1: current storage in glacier [mm]
    :param S2: current storage in snowpack [mm]
    :param St: storage in S2 threshold below which glacier melt occurs [mm]
    :param dt: time step size [d]
    :param varargin: smoothing variable r (default 0.01), e (default 5.00)
    :return:
    """
    out = np.multiply(np.amin(np.amax(p1 * (T - p2), 0), S1 / dt), smooth_threshold_storage_logistic(S2, St, **varargin))
    return out
