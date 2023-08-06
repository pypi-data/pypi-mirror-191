import numpy as np
    
def phenology_1(T = None,p1 = None,p2 = None,Ep = None): 
    """
    Phenology-based correction factor for potential evapotranspiration (returns flux [mm/d])
    :param T: current temperature [oC]
    :param p1: temperature threshold where evaporation stops [oC]
    :param p2: temperature threshold above which corrected Ep = Ep
    :param Ep: current potential evapotranspiration [mm/d]
    :return:
    """
    out = np.amin(1,np.amax(0,(T - p1) / (p2 - p1))) * Ep
    return out


def phenology_2(p1=None, p2=None, p3=None, t=None, t_max=None, dt=None):
    """
    Phenology-based maximum interception capacity (returns store size [mm])
    Constraints:  Implicit assumption: 0 <= p2 <= 1
    :param p1: mean interception capacity [mm]
    :param p2: seasonal change as fraction of the mean [-]
    :param p3: time of maximum store size [d]
    :param t: current time step [-]
    :param t_max: seasonal length [d]
    :param dt: time step size [d]
    :return:
    """
    out = p1 * (1 + p2 * np.sin(2 * np.pi * (t * dt - p3) / t_max))
    return out