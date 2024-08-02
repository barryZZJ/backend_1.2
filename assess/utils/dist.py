import numpy as np
from scipy.spatial.distance import pdist


def seuclidDisSim(x, y):
    """
    标准欧氏距离，取值 [0,+∞)
    """
    return pdist(np.vstack([x, y]), 'seuclidean')[0]


def manhattanDisSim(x, y):
    """
    曼哈顿距离
    """
    return np.sum(np.abs(x - y))


def chebyshevDisSim(x, y):
    """
    切比雪夫距离
    """
    return np.linalg.norm(x - y, ord=np.inf)


def minkowskiDisSim(x, y, p):
    """
    明可夫斯基距离
    """
    sumvalue = np.sum(np.power(np.abs(x - y), p))
    tmp = 1 / float(p)
    return sumvalue ** tmp


def mahalanobisDisSim(x, y):
    """
    马氏距离
    """
    npvec1, npvec2 = np.array(x), np.array(y)
    npvec = np.array([npvec1, npvec2])
    sub = npvec.T[0] - npvec.T[1]
    inv_sub = np.linalg.inv(np.cov(npvec1, npvec2))
    return np.sqrt(np.dot(inv_sub, sub).dot(sub.T))
