import numpy as np


def effective_1(In1=None, In2=None):
    """
    General effective flow (returns flux [mm/d]), Constraints: In1 > In2
    :param In1: first flux [mm/d]
    :param In2: second flux [mm/d]
    :return:
    """
    out = np.amax(In1 - In2, 0)
    return out
