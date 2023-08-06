import numpy as np


def route(flux_in, uh):
    return uh[0, 0] * flux_in + uh[1, 0]


def update_uh(uh, flux_in):
    """
    UPDATE_UH calculates new still-to-flow values of a unit hydrograph
    at the based on a flux routed through it at this timestep.
    Args:
        uh: unit hydrograph [nx2]
            uh's first row contains coeficients to splut flow at each
            of n timesteps forward, the second row contains still-to-flow values.
        flux_in: input flux

    Returns: update unit hydrograph [nx2]
    update_uh does not change the first row
    """
    uh[1, :] = uh[0, :] * flux_in + uh[1, :]
    uh[1, :-1] = uh[1, 1:]
    uh[1, -1] = 0
    return uh


def uh_1_half(d_base, delta_t) -> np.ndarray:
    """
    uh_1_half Unit Hydrograph [days] with half a bell curve. GR4J-based
    Args:
        d_base: time base of routing delay [d]
        delta_t: time step size [d]

    Returns: unit hydrograph [nx2]
               uh's first row contains coeficients to splut flow at each
               of n timesteps forward, the second row contains zeros now,
               these are the still-to-flow values.
   Unit hydrograph spreads the input volume over a time period x4.
   Percentage of input returned only increases.
    """
    delay = d_base / delta_t
    # any value below t = 1 means no delay, but zero leads to problems
    if delay == 0:
        delay = 1
    tt = np.arange(0, int(np.ceil(delay)))

    # ordinates [days]

    # EMPTIES
    SH = np.zeros((len(tt) + 1))
    SH[0] = 0
    UH = np.zeros((2, len(tt)))

    # UNIT HYDROGRAPH
    for t in tt:
        if t + 1 < delay:
            SH[t + 1] = ((t + 1) / delay) ** (5.0 / 2)
        else:
            if t + 1 >= delay:
                SH[t + 1] = 1
        UH[0, t] = SH[t + 1] - SH[t]
    UH[1, :] = np.zeros(len(tt))
    return UH


def uh_2_full(d_base=None, delta_t=None) -> np.ndarray:
    """
    uh_2_full Unit Hydrograph [days] with a full bell curve. GR4J-based
    Args:
        d_base: time base of routing delay [d]
        delta_t: time step size [d]

    Returns: unit hydrograph [nx2]
              uh's first row contains coeficients to splut flow at each
              of n timesteps forward, the second row contains zeros now,
              these are the still-to-flow values.
      Unit hydrograph spreads the input volume over a time period 2*x4.
      Percentage of input returned goes up (till x4), then down again.

    """
    # TIME STEP SIZE
    delay = d_base / delta_t
    tt = np.arange(0, int(2 * np.ceil(delay)))

    # EMPTIES
    SH = np.zeros((len(tt) + 1))
    SH[0] = 0
    UH = np.zeros((2, len(tt)))
    # UNIT HYDROGRAPH
    for t in tt:
        if t + 1 <= delay:
            SH[t + 1] = 0.5 * ((t + 1) / delay) ** (5.0 / 2)
        else:
            if ((t + 1) > delay) & ((t + 1) < 2 * delay):
                SH[t + 1] = 1 - 0.5 * (2 - (t + 1) / delay) ** (5.0 / 2)
            else:
                if (t + 1) >= 2 * delay:
                    SH[t + 1] = 1
        UH[0, t] = SH[t + 1] - SH[t]
    return UH


def uh_3_half(d_base=None, delta_t=None):
    """
    Unit Hydrograph [days] with half a triangle (linear)
    Args:
        d_base: time base of routing delay [d]
        delta_t: time step size [d]

    Returns: unit hydrograph [nx2]
              uh's first row contains coeficients to splut flow at each
              of n timesteps forward, the second row contains zeros now,
              these are the still-to-flow values.
    Unit hydrograph spreads the input volume over a time period delay.
    Percentage of input returned only increases.
    """
    # TIME STEP SIZE
    delay = d_base / delta_t
    if delay == 0:
        delay = 1

    # but zero leads to problems
    tt = np.arange(0, int(np.ceil(delay)))

    # ordinates [days]

    # UNIT HYDROGRAPH
    # The area under the unit hydrograph by definition sums to 1. Thus the area
    # is S(t=0 to t = delay) t*[ff: fraction of flow to move per time step] dt
    # Analytical solution is [1/2 * t^2 + c]*ff, with c = 0. Thus the fraction
    # of flow step size is:
    ff = 1 / (0.5 * delay ** 2)
    # EMPTIES
    UH = np.zeros((2, len(tt)))
    # UNIT HYDROGRAPH
    for t in tt:
        if t + 1 <= delay:
            UH[0, t] = ff * (0.5 * (t + 1) ** 2 - 0.5 * t ** 2)
        else:
            UH[0, t] = ff * (0.5 * delay ** 2 - 0.5 * t ** 2)

    UH[1, :] = np.zeros(len(tt))
    return UH


def uh_4_full(d_base=None, delta_t=None):
    """
    uh_4_half Unit Hydrograph [days] with a triangle (linear)
    Args:
        d_base: time base of routing delay [d]
        delta_t: time step size [d]

    Returns: unit hydrograph [nx2]
               uh's first row contains coeficients to splut flow at each
               of n timesteps forward, the second row contains zeros now,
               these are the still-to-flow values.
    Unit hydrograph spreads the input volume over a time period delay.
    Percentage runoff goes up, peaks, and goes down again.
    """
    from scipy import integrate

    # TIME STEP SIZE
    delay = d_base / delta_t
    if delay == 0:
        delay = 1

    # but zero leads to problems
    tt = np.arange(0, int(np.ceil(delay)))

    # ordinates [days]

    # UNIT HYDROGRAPH
    # The area under the unit hydrograph by definition sums to 1. Thus the area
    # is S(t=0 to t = delay) t*[ff: fraction of flow to move per time step] dt
    # Analytical solution is [1/2 * t^2 + c]*ff, with c = 0.
    # Here, we use two half triangles t make one big one, so the area of half a
    # triangle is 0.5. Thus the fraction of flow step size is:
    ff = 0.5 / (0.5 * (0.5 * delay) ** 2)
    d50 = 0.5 * delay

    # TRIANGLE FUNCTION
    def tri(t=None):
        return np.amax(np.multiply(np.multiply(ff, (t - d50)), np.sign(d50 - t)) + np.multiply(ff, d50), 0)

    # EMPTIES
    UH = np.zeros((2, len(tt)))
    # UNIT HYDROGRAPH
    for t in tt:
        UH[0, t] = integrate.quad(tri, t, t + 1)[0]

    # ENSURE UH SUMS TO 1
    tmp_diff = 1 - np.sum(UH)
    tmp_weight = UH[0, :] / np.sum(UH)
    UH[0, :] = UH[0, :] + np.multiply(tmp_weight, tmp_diff)
    UH[1, :] = np.zeros(len(tt))
    return UH


def uh_5_half(d_base=None, delta_t=None):
    """
    uh_5_half Unit Hydrograph [days] with half a triangle (exponential decay)
    Args:
        d_base: time base of routing delay [d]
        delta_t: time step size [d]

    Returns: unit hydrograph [nx2]
               uh's first row contains coeficients to splut flow at each
               of n timesteps forward, the second row contains zeros now,
               these are the still-to-flow values.
    Unit hydrograph spreads the input volume over a time period delay.
    Percentage of input returned only decreases.
    """
    from scipy import integrate
    # TIME STEP SIZE
    delay = d_base / delta_t
    if delay == 0:
        delay = 1

    # but zero leads to problems
    tt = np.arange(0, int(np.ceil(delay)))

    # ordinates [days]
    # UNIT HYDROGRAPH
    # The Unit Hydrograph follows exponential decay y=exp(-x). For a given
    # delay time, the fraction of flow per time step is thus the integral of
    # t-1 to t of the exponential decay curve. The curve has range [0,Inf>.
    # We impose the arbitrary boundary of [0,7] here (exp(-7) = 9e-4) as the
    # point where the decay curve 'ends'. This allows to divide the range [0,7]
    # in n delay steps, and so calculate the UH.

    # Find integral limits
    stepsize = (7 - 0) / delay

    # calculated, divided by required
    # number of delay steps
    limits = np.arange(0, 7, stepsize)
    limits = np.append(limits, 7)
    # EMPTIES
    UH = np.zeros((2, len(tt)))

    for t in tt:
        UH[0, t] = integrate.quad(lambda x=None: np.exp(- x), limits[t], limits[t + 1])[0]

    # ACCOUNT FOR <7,Inf> PART OF THE CURVE (i.e. add the missing tail end of
    # the curve to the last delay step, to ensure that 100# of flow is routed).
    UH[0, -1] = UH[0, -1] + (1 - np.sum(UH))
    UH[1, :] = np.zeros(len(tt))
    return UH


def uh_6_gamma(n=None, k=None, delta_t=None):
    """
    Unit Hydrograph [days] from gamma function.
    Args:
        n: shape parameter [-]
        k: time delay for flow reduction by a factor e [d]
        delta_t: time step size [d]

    Returns: unit hydrograph [nx2]
               uh's first row contains coeficients to splut flow at each
               of n timesteps forward, the second row contains zeros now,
               these are the still-to-flow values.
    """
    from scipy import integrate, special

    UH_list = []
    t = 0
    while True:
        # calculate the pdf of the gamma distr at this timestep
        UH_t = integrate.quad(
            lambda x=None: np.multiply(np.multiply(
                1.0 / (np.multiply(k, special.gamma(n))), (x / k) ** (n - 1)),
                np.exp(- 1.0 * x / k)), (t - 1) * delta_t, t * delta_t)[0]
        UH_list.append(UH_t)
        # if the new value of the UH is less than 0.1# of the peak, end the loop.
        # NOTE: this works because the gamma distr is monomodal, hence on
        # the way to the peak UH(t) = max(UH) > max(UH) * .001.
        if UH_t < (max(UH_list) * 0.001):
            break
        # go to the next step
        t = t + 1
    UH = np.zeros((2, len(UH_list)))
    UH[0, :] = UH_list
    # Account for the truncated part of the UH.
    # find probability mass to the right of the cut-off point
    tmp_excess = 1 - np.sum(UH[0, :])
    # find relative size of each time step
    tmp_weight = UH[0, :] / np.sum(UH[0, :])
    # distribute truncated probability mass proportionally to all elements
    # of the routing vector
    UH[0, :] = UH[0, :] + np.multiply(tmp_weight, tmp_excess)
    UH[1, :] = np.zeros(len(UH_list))
    return UH


def uh_7_uniform(d_base=None, delta_t=None):
    """
    Unit Hydrograph [days] with uniform spread
    Args:
        d_base: time base of routing delay [d]
        delta_t: time step size [d]

    Returns: unit hydrograph [nx2]
                  uh's first row contains coeficients to splut flow at each
                  of n timesteps forward, the second row contains zeros now,
                  these are the still-to-flow values.
    """
    # TIME STEP SIZE
    delay = d_base / delta_t
    tt = np.arange(0, int(np.ceil(delay)))

    # EMPTIES
    UH = np.multiply(np.nan, np.zeros((2, len(tt))))
    # FRACTION FLOW
    ff = 1 / delay

    # UNIT HYDROGRAPH
    for t in tt:
        if t + 1 < delay:
            UH[0, t] = ff
        else:
            UH[0, t] = np.mod(delay, t) * ff

    UH[1, :] = np.zeros(len(tt))
    return UH


def uh_8_delay(t_delay=None, delta_t=None):
    # uh_8_delay Unit Hydrograph [days] with a pure delay (no transformation).

    # Copyright (C) 2019, 2021 Wouter J.M. Knoben, Luca Trotter
    # This file is part of the Modular Assessment of Rainfall-Runoff Models
    # Toolbox (MARRMoT).
    # MARRMoT is a free software (GNU GPL v3) and distributed WITHOUT ANY
    # WARRANTY. See <https://www.gnu.org/licenses/> for details.

    #   Inputs
    #   t_delay - flow delay [d]
    #   delta_t - time step size [d]

    #   Output
    #   UH      - unit hydrograph [nx2]
    #               uh's first row contains coeficients to splut flow at each
    #               of n timesteps forward, the second row contains zeros now,
    #               these are the still-to-flow values.

    #   Unit hydrograph shifts the input volume over a time period.
    #   Input is spread over maximum 2 time steps.
    #   I.e. t_delay = 3.8 [days], delta_t = 1:
    #   UH(1) = 0.00  [# of inflow]
    #   UH(2) = 0.00
    #   UH(3) = 0.00
    #   UH(4) = 0.20
    #   UH(5) = 0.80

    # TIME STEP SIZE
    delay = t_delay / delta_t
    # UNIT HYDROGRAPH
    # The input is only shifted in time, not transformed, so we only need two
    # ordinates:
    ord1 = 1 - t_delay + int(np.floor(t_delay))
    ord2 = t_delay - int(np.floor(t_delay))
    # Flow appears from this time step (t+t_start; a delay of 1 time step means
    # flow doesn't appear on t=1, but starts on t=1+1):
    t_start = int(np.floor(delay))
    UH = np.zeros((2, t_start + 1 + 1))
    # Unit Hydrograph
    UH[0, t_start] = ord1
    UH[0, t_start + 1] = ord2
    return UH


if __name__ == '__main__':
    uh = uh_8_delay(3.8, 1)
