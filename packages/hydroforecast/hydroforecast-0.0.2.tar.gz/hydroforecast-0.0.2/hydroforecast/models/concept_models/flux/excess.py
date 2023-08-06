import numpy as np


def excess_1(So=None, Smax=None, dt=None):
    """
    Storage excess when store size changes (returns flux [mm/d])
    Constraints:  f >= 0
    :param So: 'old' storage [mm]
    :param Smax: 'new' maximum storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax((So - Smax) / dt, 0)
    return out
