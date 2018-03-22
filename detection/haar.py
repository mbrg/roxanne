import numpy as np
import cv2
from . import *
from detection.projective import pixel_to_world, world_to_pixel
from detection.locate_ball_2d import find_xyr


# globals
soccer_cascade = cv2.CascadeClassifier(SOCCER['cascade'])


class VideoCap(object):
    def __init__(self, cam=0, soft_exit=False):
        self._cam = cam
        self.cap = None
        self._soft_exit = soft_exit

    def __enter__(self):
        self.cap = cv2.VideoCapture(self._cam)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()
        if not self._soft_exit:
            cv2.destroyAllWindows()


def detect_circle(img):
    x, y, r = 1, 1, 1
    return x, y, r


def find_xyr(img, rec):
    u = rec[2] / 2
    v = rec[3] / 2
    r = min([u, v])
    return u, v, r


def calc_dist(image_radius):
    known_radius_cm = (SOCCER['min_radius_cm'] + SOCCER['max_radius_cm']) / 2
    return (known_radius_cm * FOCAL_LENGTH) / image_radius


def process_frame(img, draw_rec=False, draw_circ=False):
    """
    Pixel Coordinates - (u,v), depth
    World Coordinates - X,Y,Z
    """

    # defaults
    num_found = 0
    euc_coors = []

    # detect soccer
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    soccers = soccer_cascade.detectMultiScale(gray, 1.3, 5)

    for nw_x, nw_y, rec_w, rec_h in soccers:
        num_found += 1

        # bound soccer with a rectangle
        if draw_rec:
            cv2.rectangle(img, (nw_x, nw_y), (nw_x + rec_w, nw_y + rec_h), (255, 0, 0), 2)

        # detect soccer boundary
        soccer_crop = gray[nw_y: nw_y + rec_h, nw_x: nw_x + rec_w]
        u, v, radius = find_xyr(soccer_crop, [nw_x, nw_y, rec_w, rec_h])
        if draw_circ:
            cv2.circle(img, (nw_x + int(u), nw_y + int(v)), int(radius), (255, 0, 0), 2)

        # calculate distance
        depth = calc_dist(radius)

        # coordinates
        euc_coors.append(pixel_to_world(u, v, depth))

    return img, num_found, euc_coors


def video(ret_first_cap=False, draw_rec=False, draw_circ=False):

    img_cache = None
    locations = np.array([[0, 0, 0],])

    with VideoCap(0) as vidcap:

        while True:
            try:
                # capture image
                ret, img = vidcap.cap.read()

                # process
                img, num_found, euc_coors = process_frame(img, draw_rec, draw_circ)

                # in case ball wasn't found, take last known coordinates
                if num_found == 0:
                    euc_coors = locations[-1, :]

                # in case multiple balls were found, take the one closest to last known location
                if num_found > 1:
                    options = [np.linalg.norm(c - locations[-1, :]) for c in euc_coors]
                    euc_coors = euc_coors[np.argmin(options)]

                if ret_first_cap and num_found > 0:
                    img_cache = img
                    break

                # plot
                cv2.imshow('img', img)
                _ = cv2.waitKey(30) & 0xff

            except KeyboardInterrupt:
                break

    return img_cache