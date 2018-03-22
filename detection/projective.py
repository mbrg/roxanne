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


def world_to_pixel(x, y, z, d):
    """
    Given World coordinates (x, y, z)
    Return pixel coordinates
    """

    # world coordinates
    wrld = np.array([x, y, z])

    # pixel homogeneous coordinates
    pxl = K * (wrld / d)

    return pxl


