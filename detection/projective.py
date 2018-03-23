from . import *
import numpy as np


K = np.array(K)


def pixel_to_world(u, v, d):
    """
    Given Pixel coordinates (u, v) and depth d
    Return world Euclidean coordinates
    """

    # pixel homogeneous coordinates
    pxl = np.array([u, v, 1])

    # world coordinates
    wrld = np.dot(np.linalg.inv(K), pxl) * d

    return wrld


def world_to_pixel(wrld_coor):
    """
    Given World coordinates (x, y, z)
    Return pixel coordinates
    """

    # pixel homogeneous coordinates
    #print(wrld_coor.shape)
    pxl = np.einsum('ij,kj',K, wrld_coor)
    pxl = np.divide(pxl, pxl[:, 2].reshape((pxl.shape[0], 1)) * np.ones((1, 3))  + EPS)

    return pxl


