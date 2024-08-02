import numpy as np
from scipy.stats import differential_entropy
from sklearn.feature_selection import mutual_info_regression
from sklearn.metrics import mutual_info_score
from sklearn.metrics.cluster import entropy


def mutual_info_discrete(datacol, datacol_disturbed):
    return mutual_info_score(datacol.flatten(), datacol_disturbed.flatten())


def rel_mutual_info_discrete(datacol, datacol_disturbed, mi_max=None):
    """使用mutual_info_score计算mi，适合离散值"""
    datacol_arr = datacol.flatten()
    mi = np.asarray(mutual_info_score(datacol_arr, datacol_disturbed.flatten()))
    mi_max = mi_max or np.asarray(mutual_info_score(datacol_arr, datacol.flatten()))
    rmi = mi / mi_max
    return rmi
    # return mi, rmi, mi_max


def mutual_info_continuous(datacol, datacol_disturbed):
    return mutual_info_regression(datacol.reshape(-1, 1), datacol_disturbed.flatten())


def rel_mutual_info_continuous(datacol, datacol_disturbed, mi_max=None):
    """使用mutual_info_regression计算mi，适合连续值"""
    datacol_arr = datacol.reshape(-1, 1)
    mi = mutual_info_regression(datacol_arr, datacol_disturbed.flatten())
    mi_max = mi_max or mutual_info_regression(datacol_arr, datacol.flatten())
    rmi = mi / mi_max
    return rmi


def entropy_discrete(data):
    """适用于离散值"""
    return entropy(data)


def entropy_discrete2(data):
    """适用于离散值，跟上面的计算结果一致"""
    unique_values, counts = np.unique(data, return_counts=True)
    probabilities = counts / len(data)
    res = -np.sum(probabilities * np.log(probabilities))
    return res


def entropy_continuous(data):
    cx = np.histogram(data, 'auto')[0]

    c_normalized = cx / float(np.sum(cx))
    c_normalized = c_normalized[np.nonzero(c_normalized)]
    h = -sum(c_normalized * np.log(c_normalized))
    return h


def differential_entropy_continuous(data):
    """适用于连续值"""
    return differential_entropy(data)
