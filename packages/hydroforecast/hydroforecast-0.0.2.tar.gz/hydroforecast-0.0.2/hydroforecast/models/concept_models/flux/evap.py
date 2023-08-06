import numpy as np

from .smoother import smooth_threshold_storage_logistic


def evap_1(S=None, Ep=None, dt=None):
    """
    Evaporation at the potential rate
    Constraints:  f <= S/dt
    :param S: current storage [mm]
    :param Ep: potential evaporation rate [mm/d]
    :param dt: time step size
    :return:
    """
    out = np.amin(S / dt, Ep)
    return out


def evap_2(p1=None, S=None, Smax=None, Ep=None, dt=None):
    """
    Evaporation at a scaled, plant-controlled rate
    Constraints:  f <= Ep
                  f <= S/dt
    :param p1: plant-controlled base evaporation rate [mm/d]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.array([p1 * S / Smax, Ep, S / dt]))
    return out


def evap_3(p1=None, S=None, Smax=None, Ep=None, dt=None):
    """
    Evaporation based on scaled current water storage and wilting point
    Constraints:  f <= Ep
                  f <= S/dt
    :param p1: wilting point as fraction of Smax [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.array([S / (p1 * Smax) * Ep, Ep, S / dt]))
    return out


def evap_4(Ep=None, p1=None, S=None, p2=None, Smax=None, dt=None):
    """
    Constrained, scaled evaporation if storage is above a wilting point
    Constraints:  f <= S/dt
    :param Ep: potential evapotranspiration rate [mm/d]
    :param p1: scaling parameter [-]
    :param p2: wilting point as fraction of Smax [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.multiply(Ep, np.amax(0, p1 * (S - np.multiply(p2, Smax)) / (Smax - np.multiply(p2, Smax)))), S / dt)
    return out


def evap_5(p1=None, S=None, Smax=None, Ep=None, dt=None):
    """
    Evaporation from bare soil scaled by relative storage
    Constraints:  Ea <= Ep
                  Ea <= S/dt
    :param p1: fraction of area that is bare soil [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(np.amin(np.multiply(np.multiply((1 - p1), S) / Smax, Ep), S / dt), 0)
    return out


def evap_6(p1=None, p2=None, S=None, Smax=None, Ep=None, dt=None):
    """
    Transpiration from vegetation at the potential rate if storage is above a wilting point and scaled by relative storage if not
    Constraints:  Ea <= Ep
                  Ea <= S/dt
    :param p1: fraction vegetated area [-]
    :param p2: wilting point as fraction of Smax
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.array([np.multiply(p1, Ep), p1 * Ep * S / (p2 * Smax), S / dt]))
    return out


def evap_7(S=None, Smax=None, Ep=None, dt=None):
    """
    Evaporation scaled by relative storage
    Constraints:  f <= S/dt
    :param S: current storage [mm]
    :param Smax: maximum contributing storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = min(np.multiply(S / Smax, Ep), S / dt)
    return out


def evap_8(S1=None, S2=None, p1=None, p2=None, Ep=None, dt=None):
    """
    Transpiration from vegetation, at potential rate if soil moisture is above the wilting point, and linearly
    decreasing if not. Also scaled by relative storage across all stores
    Constraints:  f <= S/dt
                  f >= 0
    :param S1: current storage in store 1 [mm]
    :param S2: current storage in store 2 [mm]
    :param p1: fraction vegetated area [-]
    :param p2: wilting point [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(np.amin(np.array([S1 / (S1 + S2) * p1 * Ep, S1 / (S1 + S2) * S1 / p2 * p1 * Ep, S1 / dt])), 0)
    return out


def evap_9(S1=None, S2=None, p1=None, p2=None, Ep=None, dt=None):
    """
     Evaporation from bare soil scaled by relative storage and by relative water availability across all stores all stores
    Constraints:  f <= S/dt
                  f >= 0
    :param S1: current storage in store 1 [mm]
    :param S2: current storage in store 2 [mm]
    :param p1: fraction vegetated area [-]
    :param p2: wilting point [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(np.amin(S1 / (S1 + S2) * (1 - p1) * S1 / (p2 - S2) * Ep, S1 / dt), 0)
    return out


def evap_10(p1=None, S=None, Smax=None, Ep=None, dt=None):
    """
    Evaporation from bare soil scaled by relative storage
    Constraints:  Ea <= Ep
                  Ea <= S/dt
    :param p1: fraction of area that is bare soil [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(np.amin(np.multiply(np.multiply(p1, S) / Smax, Ep), S / dt), 0)
    return out


def evap_11(S=None, Smax=None, Ep=None):
    """
    Evaporation quadratically related to current soil moisture
    Constraints:  f >= 0
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :return:
    """
    out = np.amax(0, (2 * S / Smax - (S / Smax) ** 2) * Ep)
    return out


def evap_12(S=None, p1=None, Ep=None):
    """
    Evaporation from deficit store, with exponential decline as deficit goes below a threshold
    :param S: current storage [mm]
    :param p1: wilting point [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :return:
    """
    out = np.amin(1, np.exp(2 * (1 - S / p1))) * Ep
    return out


def evap_13(p1=None, p2=None, Ep=None, S=None, dt=None):
    """
    Exponentially scaled evaporation
    Constraints:  f <= S/dt
    :param p1: linear scaling parameter [-]
    :param p2: exponential scaling parameter [-]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param S: current storage [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin((p1 ** p2) * Ep, S / dt)
    return out


def evap_14(p1=None, p2=None, Ep=None, S1=None, S2=None, S2min=None, dt=None):
    """
    Exponentially scaled evaporation that only activates if another store goes below a certain threshold
    Constraints:  f <= S1/dt
    :param p1: linear scaling parameter [-]
    :param p2: exponential scaling parameter [-]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param S1: current storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :param S2min: threshold for evaporation deactivation [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.multiply(np.amin((p1 ** p2) * Ep, S1 / dt), smooth_threshold_storage_logistic(S2, S2min))
    return out


def evap_15(Ep=None, S1=None, S1max=None, S2=None, S2min=None, dt=None):
    """
    Scaled evaporation if another store is below a threshold
    Constraints:  f <= S1/dt
    :param Ep: potential evapotranspiration rate [mm/d]
    :param S1: current storage in S1 [mm]
    :param S1max: maximum storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :param S2min: maximum storage in S2 [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.multiply((S1 / S1max * Ep), smooth_threshold_storage_logistic(S2, S2min, S1 / dt)))
    return out


def evap_16(p1=None, S1=None, S2=None, S2min=None, Ep=None, dt=None):
    """
    Scaled evaporation if another store is below a threshold
    Constraints:  f <= S1/dt
    :param p1: linear scaling parameter [-]
    :param S1: current storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :param S2min: threshold S2 storage for evaporation occurence [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.multiply((np.multiply(p1, Ep)), smooth_threshold_storage_logistic(S2, S2min)), S1 / dt)
    return out


def evap_17(p1=None, S=None, Ep=None):
    """
    Scaled evaporation from a store that allows negative values
    :param p1: linear scaling parameter [mm-1]
    :param S: current storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :return:
    """
    out = np.multiply(1.0 / (1 + np.exp(np.multiply(- 1.0 * p1, S))), Ep)
    return out


def evap_18(p1=None, p2=None, p3=None, S=None, Ep=None):
    """
    Exponentially declining evaporation from deficit store
    :param p1: linear scaling parameter [-]
    :param p2: linear scaling parameter [-]
    :param p3: storage scaling parameter [mm]
    :param S: current storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :return:
    """
    out = np.multiply(np.multiply(p1, np.exp(np.multiply(- 1.0 * p2, S) / p3)), Ep)
    return out


def evap_19(p1=None, p2=None, S=None, Smax=None, Ep=None, dt=None):
    """
    Non-linear scaled evaporation
    Constraints:  f <= Ep
                  f <= S/dt
    :param p1: linear scaling parameter [-]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.array([S / dt, Ep, np.multiply(np.multiply(p1, np.amax(0, S / Smax) ** (p2)), Ep)]))
    return out


def evap_20(p1=None, p2=None, S=None, Smax=None, Ep=None, dt=None):
    """
    Evaporation limited by a maximum evaporation rate and scaled below a wilting point
    Constraints:  f <= Ep
                  f <= S/dt
    :param p1: maximum evaporation rate [mm/d]
    :param p2: wilting point as fraction of Smax [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.array([np.multiply(p1, S) / (np.multiply(p2, Smax)), Ep, S / dt]))
    return out


def evap_21(p1=None, p2=None, S=None, Ep=None, dt=None):
    """
    Threshold-based evaporation with constant minimum rate
    Constraints:  f <= S/dt
    :param p1: wilting point (1st threshold) [mm]
    :param p2: 2nd threshold as fraction of wilting point [-]
    :param S: current storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.multiply(np.amax(p2, np.amin(S / p1, 1)), Ep), S / dt)
    return out


def evap_22(p1=None, p2=None, S=None, Ep=None, dt=None):
    """
    Threshold-based evaporation rate
    Constraints:  f <= S/dt
    :param p1: wilting point [mm]
    :param p2: 2nd (lower) threshold [mm]
    :param S: current storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(S / dt, np.amax(0, np.amin(np.multiply((S - p1) / (p2 - p1), Ep), Ep)))
    return out


def evap_23(p1=None, p2=None, S=None, Smax=None, Ep=None, dt=None):
    # evap_23 combines evap_5 (evaporation) and evap_6 (transpiration)

    # Copyright (C) 2021 Clara Brandes, Luca Trotter
    # This file is part of the Modular Assessment of Rainfall-Runoff Models
    # Toolbox (MARRMoT).
    # MARRMoT is a free software (GNU GPL v3) and distributed WITHOUT ANY
    # WARRANTY. See <https://www.gnu.org/licenses/> for details.

    # Flux function
    # ------------------

    # @(Inputs):    p1   -
    #               p2   -
    #               S    -
    #               Smax -
    #               Ep   -
    #               dt   -
    """
    Transpiration from vegetation at the potential rate if storage is above field capacity and scaled by relative
    storage if not (similar to evap_6), addition of Evaporation from bare soil scaled by relative storage (similar to evap_5)
    Constraints:  Ea <= Ep
                  Ea <= S/dt
    :param p1: fraction vegetated area [-] (0...1)
    :param p2: field capacity coefficient[-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param Ep: potential evapotranspiration rate [mm/d]
    :param dt: time step size [d]
    :return:
    """
    out = np.amin(np.array([np.multiply(p1, Ep) + np.multiply(np.multiply((1 - p1), S) / Smax, Ep),
                            p1 * Ep * S / (p2 * Smax) + np.multiply(np.multiply((1 - p1), S) / Smax, Ep), S / dt]))
    return out
