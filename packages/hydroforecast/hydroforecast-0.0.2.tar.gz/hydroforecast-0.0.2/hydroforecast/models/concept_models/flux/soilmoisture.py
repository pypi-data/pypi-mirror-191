import numpy as np

from .smoother import smooth_threshold_storage_logistic


def soilmoisture_1(S1=None, S1max=None, S2=None, S2max=None):
    """
    Water rebalance to equal relative storage (2 stores)
    :param S1: current storage in S1 [mm]
    :param S1max: maximum storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :param S2max: maximum storage in S2 [mm]
    :return:
    """
    out = np.multiply(((np.multiply(S2, S1max) - np.multiply(S1, S2max)) / (S1max + S2max)),
                      smooth_threshold_storage_logistic(S1 / S1max, S2 / S2max))
    return out


def soilmoisture_2(S1=None, S1max=None, S2=None, S2max=None, S3=None, S3max=None):
    """
    Water rebalance to equal relative storage (3 stores)
    :param S1: current storage in S1 [mm]
    :param S1max: maximum storage in S1 [mm]
    :param S2: current storage in S2 [mm]
    :param S2max: maximum storage in S2 [mm]
    :param S3: current storage in S3 [mm]
    :param S3max: maximum storage in S3 [mm]
    :return:
    """
    out = np.multiply((np.multiply(S2, (np.multiply(S1, (S2max + S3max)) + np.multiply(S1max, (S2 + S3)))) / (
        np.multiply((S2max + S3max), (S1max + S2max + S3max)))), smooth_threshold_storage_logistic(S1 / S1max, (S2 + S3) / (S2max + S3max)))
    return out
