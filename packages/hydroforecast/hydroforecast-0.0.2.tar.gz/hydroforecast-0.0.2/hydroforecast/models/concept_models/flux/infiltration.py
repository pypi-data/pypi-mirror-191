import numpy as np

from .smoother import smooth_threshold_storage_logistic


def infiltration_1(p1=None, p2=None, S=None, Smax=None, fin=None):
    """
    Infiltration as exponentially declining based on relative storage
    :param p1: maximum infiltration rate [mm,/d]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param fin: size of incoming flux [mm/d]
    :return:
    """
    out = np.amin(np.multiply(p1, np.exp((- 1 * p2 * S) / Smax)), fin)
    return out


def infiltration_2(p1=None, p2=None, S1=None, S1_max=None, flux=None, S2=None, dt=None):
    """
    Infiltration as exponentially declining based on relative storage
    Constraints:  0 <= f <= S2/dt
    :param p1: maximum infiltration rate [mm,/d]
    :param p2: exponential scaling parameter [-]
    :param S1: current storage in S1 [mm]
    :param S1_max: maximum storage in S1 [mm]
    :param flux: reduction of infiltration rate by infiltration demand already fulfilled elsewhere [mm/d]
    :param S2: storage available for infiltration [mm]
    :param dt: time step size [d]
    :return:
    """
    out = np.amax(np.amin((np.multiply(p1, np.exp(- 1 * p2 * S1 / S1_max))) - flux, S2 / dt), 0)
    return out


def infiltration_3(In=None, S=None, S_max=None, varargin=None):
    # infiltration_3

    # Copyright (C) 2019, 2021 Wouter J.M. Knoben, Luca Trotter
    # This file is part of the Modular Assessment of Rainfall-Runoff Models
    # Toolbox (MARRMoT).
    # MARRMoT is a free software (GNU GPL v3) and distributed WITHOUT ANY
    # WARRANTY. See <https://www.gnu.org/licenses/> for details.

    # Flux function
    # ------------------
    # Description:
    # Constraints:  -
    # @(Inputs):    In   -
    #               S    -
    #               Smax -
    #               varargin(1) -
    #               varargin(2) - smoothing variable
    """
    Infiltration to soil moisture of liquid water stored in snow pack
    :param In: incoming flux [mm/d]
    :param S: current storage [mm]
    :param S_max: maximum storage [mm]
    :param varargin: smoothing variable r (default 0.01), e (default 5.00)
    :return:
    """
    out = np.multiply(In, (1 - smooth_threshold_storage_logistic(S, S_max, *varargin)))
    return out


def infiltration_4(fin=None, p1=None):
    """
    Constant infiltration rate
    Constraints:  f <= fin
    :param fin: incoming flux [mm/d]
    :param p1: Infiltration rate [mm/d]
    :return:
    """
    out = np.amin(fin, p1)
    return out


def infiltration_5(p1=None, p2=None, S1=None, S1_max=None, S2=None, S2_max=None):
    """
    Maximum infiltration rate non-linearly based on relative deficit and storage
    Constraints:  S2 >= 0     - prevents complex numbers
                  f <= 10^9   - prevents numerical issues with Inf outcomes
    :param p1: base infiltration rate [mm/d]
    :param p2: exponential scaling parameter [-]
    :param S1: current storage in S1 [mm]
    :param S1_max: maximum storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :param S2_max: maximum storage in S2 [mm]
    :return:
    """
    out = np.amax(0, np.amin(10 ** 9, np.multiply(np.multiply(p1, (1 - S1 / S1_max)), np.amax(0, S2 / S2_max) ** (- 1.0 * p2))))
    return out


def infiltration_6(p1=None, p2=None, S=None, S_max=None, fin=None):
    """
    Infiltration rate non-linearly scaled by relative storage
    Constraints:  f <= fin
    :param p1: base infiltration rate [mm/d]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param S_max: maximum contributing storage [mm]
    :param fin: incoming flux [mm/d]
    :return:
    """
    out = np.amin(np.array([fin, np.multiply(np.multiply(p1, np.amax(0, S / S_max) ** p2), fin)]))
    return out


def infiltration_7(p1=None, p2=None, S=None, S_max=None, fin=None, varargin=None):
    """
    Infiltration as exponentially declining based on relative storage
    Constraints:  f <= fin
    :param p1: maximum infiltration rate [mm,/d]
    :param p2: exponential scaling parameter [-]
    :param S: current storage [mm]
    :param S_max: maximum storage [mm]
    :param fin: size of incoming flux [mm/d]
    :param varargin: smoothing variable r (default 0.01), e (default 5.00)
    :return:
    """
    pre_smoother = (np.amin(np.multiply(p1, np.exp((- 1 * p2 * S) / S_max)), fin))
    out = np.multiply(pre_smoother, (1 - smooth_threshold_storage_logistic(S, S_max, **varargin)))
    return out


def infiltration_8(S=None, Smax=None, fin=None):
    """
    Infiltration into storage is equal the inflow when current storage is under the maximum storage,
     and zero when storage reaches maximum capacity
     Constraints:  f <= fin
    :param S: current storage [mm]
    :param Smax: maximum storage [mm]
    :param fin: size of incoming flux [mm/d]
    :return:
    """
    out = np.multiply((S < Smax), fin)
    return out
