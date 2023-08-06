import numpy as np


def smooth_threshold_storage_logistic(s, s_max, r=0.01, e=5):
    """
    %   Smooths the transition of threshold functions of the form:
    %
    %   Q = { P, if S = Smax
    %       { 0, if S < Smax
    %
    %   By transforming the equation above to Q = f(P,S,Smax,e,r):
    %   Q = P * 1/ (1+exp((S-Smax+r*e*Smax)/(r*Smax)))
    %
    %   NOTE: this function only outputs the multiplier. This needs to be
    %   applied to the proper flux utside of this function.
    %
    %   NOTE: can be applied for temperature thresholds as well (i.e. snow
    %   modules). This simply means that S becomes T, and Smax T0.

    % Check for inputs and use defaults if not provided
    % NOTE: this is not very elegant, but it is more than a factor 10 faster then:
    % if ~exist('r','var'); r = 0.01; end
    % if ~exist('e','var'); e = 5.00; end
    :param s: current storage
    :param s_max: maximum storage
    :param r: [optional] smoothing parameter rho, default = 0.01
    :param e: [optional] smoothing parameter e, default 5
    :return:
    """
    s_max = max(s_max, 0)
    if r * s_max == 0:
        return 1 / (1 + np.exp((s - s_max + r * e * s_max) / r))
    else:
        return 1 / (1 + np.exp((s - s_max + r * e * s_max) / (r * s_max)))


def smooth_threshold_temperature_logistic(T, Tt, r=0.01):
    out = 1. / (1 + np.exp((T - Tt) / (r)))
    return out
