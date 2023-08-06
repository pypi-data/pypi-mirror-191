import numpy as np


def refreeze_1(p1=None, p2=None, p3=None, T=None, S=None, dt=None):
    """
    Refreezing of stored melted snow
    Constraints:  f <= S/dt
    :param p1: reduction fraction of degree-day-factor [-]
    :param p2: degree-day-factor [mm/oC/d]
    :param p3: temperature threshold for snowmelt [oC]
    :param T: current temperature [oC]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(np.amin(p1 * p2 * (p3 - T), S / dt), 0)
    return out
