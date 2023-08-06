import numpy as np


def split_1(p1=None, In=None):
    """
    Split flow
    :param p1: fraction of flux to be diverted [-]
    :param In: incoming flux [mm/d]
    :return: flux [mm/d]
    """
    out = np.multiply(p1, In)
    return out


def split_2(p1=None, In=None):
    """
    Split flow, counterpart to split_1
    :param p1: fraction of flux to be diverted [-]
    :param In: incoming flux [mm/d]
    :return: flux [mm/d]
    """
    out = np.multiply((1 - p1), In)
    return out
