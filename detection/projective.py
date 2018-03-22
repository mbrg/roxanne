from . import *
import numpy as np


K = np.array(K)


def pixel_to_world(u, v, d):
    """
    Given Pixel coordinates (u, v) and depth d
    Return world Euclidean coordinates
    """

    # pixel homogeneous coordinates
    pxl = np.array([u, v, d])

    # world coordinates
    wrld = np.dot(np.linalg.inv(K), pxl)

    return wrld


def world_to_pixel(wrld_coor, d):
    """
    Given World coordinates (x, y, z)
    Return pixel coordinates
    """

    # pixel homogeneous coordinates
    pxl = np.matmul(K, wrld_coor.T).T
    pxl = np.divide(pxl, pxl[:, 2] + EPS)

    return pxl


