import numpy as np
    
def percolation_1(p1 = None,S = None,dt = None): 
    """
    Percolation at a constant rate
    Constraints:  f <= S/dt
    :param p1: base percolation rate [mm/d]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(p1,S / dt)
    return out


def percolation_2(p1=None, S=None, Smax=None, dt=None):
    """
    Percolation scaled by current relative storage
    Constraints:  f <= S/dt
    :param p1: maximum percolation rate [mm/d]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(S / dt, np.multiply(p1, S) / Smax)
    return out


def percolation_3(S=None, Smax=None):
    """
    Non-linear percolation (empirical)
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :return:
    """
    out = Smax ** (- 4) / 4 * (4 / 9) ** 4 * S ** 5
    return out


def percolation_4(p1=None, p2=None, p3=None, p4=None, p5=None, S=None, S_max=None, dt=None):
    """
    Demand-based percolation scaled by available moisture
    Constraints:  f <= S/dt
                  f >= 0          prevents erratic numerical behaviour
    Note: for certain extreme parameter values (very small stores, highly
    non-linear p3) and small computational errors that lead to small negative
    S values, this function behaves erratically. The max(0,S/Smax) part
    prevents this. Similarly, the first max(0,...) part prevents negative
    percolation demands as a result of small numerical errors.
    :param p1: base percolation rate [mm/d]
    :param p2: percolation rate increase due moisture deficiencies [mm/d]
    :param p3: non-linearity parameter [-]
    :param p4: summed deficiency across all model stores [mm]
    :param p5: summed capacity of model stores [mm]
    :param S: current storage in the supplying store [mm]
    :param S_max: maximum storage in the supplying store [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(0, np.amin(S / dt, np.multiply(np.amax(0, S / S_max), (np.multiply(p1, (1 + np.multiply(p2, (p4 / p5) ** (1 + p3))))))))
    return out


def percolation_5(p1=None, p2=None, S=None, S_max=None, dt=None):
    """
    Non-linear percolation
    Constraints:  f <= S/dt
                  S >= 0      prevents complex numbers
    :param p1: base percolation rate [mm/d]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param S_max: maximum contributing storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(S / dt, np.multiply(p1, ((np.amax(S, 0) / S_max) ** p2)))
    return out


def percolation_6(p1=None, p2=None, S=None, dt=None):
    """
    Threshold-based percolation from a store that can reach negative values
    Constraints:  f <= S/dt
    :param p1: maximum percolation rate
    :param p2: storage threshold for reduced percolation [mm]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(S / dt, np.multiply(p1, np.amin(1, np.amax(0, S) / p2)))
    return out