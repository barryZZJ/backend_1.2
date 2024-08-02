import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from sklearn.feature_selection import r_regression


def pearson_correlation(datacol, datacol_disturbed):
    """皮尔森相关系数，取值[-1, 1]，-1完全负相关，1时完全正相关"""
    return r_regression(datacol.reshape(-1, 1), datacol_disturbed.flatten())


def pearsonrSim(x, y):
    """
    皮尔森相似度，取值[-1, 1]，-1完全负相关，1时完全正相关，与上面的一样
    """
    return pearsonr(x, y)[0]


def spearmanrSim(x, y):
    """
    斯皮尔曼相似度，取值[-1, 1]，-1完全负相关，1时完全正相关（排序一致性）
    """
    return spearmanr(x, y)[0]


def kendalltauSim(x, y):
    """
    肯德尔相似度，取值[-1, 1]，-1完全负相关，1时完全正相关（排序一致性）
    """
    return kendalltau(x, y)[0]


def cosSim(x, y):
    """
    余弦相似度，取值[-1, 1]，-1完全负相关，1时完全正相关
    """
    tmp = np.dot(x, y)
    non = np.linalg.norm(x) * np.linalg.norm(y)
    return tmp / float(non)


def euclidDisSim(x, y):
    """
    欧几里得相似度，取值[0,1]，其中1表示完全一致，0表示不相关
    """
    return 1 / (1 + np.sqrt(np.sum(np.power(x - y, 2))))


def jaccardDisSim(x, y):
    """
    杰卡德相似度，适用于整数，取值[0,1]
    """
    res = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return res / float(union_cardinality)
