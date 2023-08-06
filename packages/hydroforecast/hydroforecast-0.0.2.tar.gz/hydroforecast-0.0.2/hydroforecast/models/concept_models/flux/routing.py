import numpy as np


def routing_1(p1=None, p2=None, p3=None, S=None, dt=None):
    """
    Threshold-based non-linear routing
    Constraints:  f <= S/dt
                  S >= 0      prevents complex numbers
    :param p1: linear scaling parameter [-]
    :param p2: exponential scaling parameter [-]
    :param p3: fractional release parameter [-]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.array([S / dt, np.multiply(p1, (np.amax(S, 0) ** p2)), np.multiply(p3, S) / dt]))
    return out
