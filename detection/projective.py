import numpy as np
from . import *


''' Calibrate Camera Transformations '''

# camera intrinsic parameters
focal = IMAGE_SIZE_X / (2 * tan(FOV * pi / 360))
cu = IMAGE_SIZE_X / 2
cv = IMAGE_SIZE_Y / 2

K = np.array([[focal, 0, cu],
              [0, focal, cv],
              [0, 0, 1]])


def pixel_to_world(u, v, d):
    """
    Given Pixel coordinates (u, v) and depth d
    Return world Euclidean coordinates
    """

    # pixel homogeneous coordinates
    pxl = np.array([u, v, 1])

    # world coordinates
    wrld = (np.linalg.inv(K) * pxl) * d

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


