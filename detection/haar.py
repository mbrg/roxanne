import numpy as np
import cv2
from . import *
from detection.projective import pixel_to_world, world_to_pixel
from detection.locate_ball_2d import find_xyr
from detection.trajectory import find_trajectory
from os.path import join
import glob

# globals
soccer_cascade = cv2.CascadeClassifier(SOCCER['cascade'])


def intable(x):
    try:
        _ = int(x)
    except ValueError:
        return False
    else:
        return True


class VideoCap(object):
    def __init__(self, cam=0, soft_exit=False):
        self._cam = cam
        self._cap = None
        self._soft_exit = soft_exit

        # run based on prerecorded images
        if not intable(cam):
            self._mode = 'prerecorded'
            self._image_gen = self.load_images()
            self._cur_image = 0
        else:
            self._mode = 'vid'

    def load_images(self, ext='.jpg'):
        return sorted(glob.glob(join(self._cam, '*%s' % ext)))

    def read(self):
        if self._mode == 'vid':
            return self._cap.read()
        else:
            cur_image = self._cur_image
            print(cur_image)
            self._cur_image = (self._cur_image + 1) % len(self._image_gen)
            img_file = self._image_gen[cur_image]
            return None, cv2.imread(img_file)

    def __enter__(self):
        if self._mode == 'vid':
            self._cap = cv2.VideoCapture(self._cam)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._mode == 'vid':
            self._cap.release()
            if not self._soft_exit:
                cv2.destroyAllWindows()


def naive_xyr(rec_w, rec_h):
    u = rec_w / 2
    v = rec_h / 2
    r = min([u, v])
    return u, v, r


def calc_dist(image_radius):
    known_radius_cm = (SOCCER['min_radius_cm'] + SOCCER['max_radius_cm']) / 2
    return (known_radius_cm * FOCAL_LENGTH) / image_radius


def process_frame(img, xyz_trans, draw_rec=False, draw_circ=False):
    """
    Pixel Coordinates - (u,v), depth
    World Coordinates - X,Y,Z
    """

    # defaults
    num_found = 0
    pix_coors = []
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
        if xyz_trans == 'naive':
            u, v, radius = naive_xyr(rec_w, rec_h)
        else:
            u, v, radius = find_xyr(soccer_crop)
        if draw_circ:
            cv2.circle(img, (nw_x + int(u), nw_y + int(v)), int(radius), (255, 0, 0), 2)

        # calculate distance
        depth = calc_dist(radius)

        # coordinates
        pix_coors.append(np.array([nw_x + u, nw_y + v, depth]))
        euc_coors.append(pixel_to_world(nw_x + u, nw_y + v, depth))

    return img, num_found, pix_coors, euc_coors


def video(xyz_trans='naive', cam=0,
          num_frames=1000000, ret_first_cap=False,
          draw_rec=False, draw_circ=False, draw_cntr=False):

    assert(xyz_trans in ('naive', 'conv'))

    img_cache = None
    pix_cache = np.array([[EPS, EPS, EPS], [EPS, EPS, EPS],])
    euc_cache = np.array([[EPS, EPS, EPS], [EPS, EPS, EPS],])
    ground_normal = np.array([EPS, 1.0, EPS]) / np.linalg.norm([EPS, 1.0, EPS])

    with VideoCap(cam) as vidcap:

        try:
            for i in range(num_frames):
                # capture image
                _, img = vidcap.read()

                # process
                img, num_found, pix_coors, euc_coors = process_frame(img, xyz_trans, draw_rec, draw_circ)

                # in case ball wasn't found, take last known coordinates
                if num_found == 0:
                    pix_coors = pix_cache[-1, :]
                    euc_coors = euc_cache[-1, :]

                if num_found == 1:
                    pix_coors = pix_coors[0]
                    euc_coors = euc_coors[0]

                # in case multiple balls were found, take the one closest to last known location
                if num_found > 1:
                    options = [np.linalg.norm(c - pix_cache[-1, :]) for c in pix_coors]
                    pix_coors = pix_coors[np.argmin(options)]
                    euc_coors = euc_coors[np.argmin(options)]

                # save coordinates
                pix_cache = np.r_[pix_cache, pix_coors.reshape((1,3))]
                euc_cache = np.r_[euc_cache, euc_coors.reshape((1,3))]

                # trajectory
                #euc_traj = find_trajectory(euc_cache[-3:, :], ground_normal, FPS)
                #pix_traj = world_to_pixel(euc_traj, pix_cache)

                if ret_first_cap and num_found > 0:
                    img_cache = img
                    break

                # draw ball centers
                if draw_cntr:
                    for i in range(pix_cache.shape[0]):
                        if any(pix_cache[i, :2] != 0):
                            cv2.circle(img, (int(pix_cache[i,0]), int(pix_cache[i,1])), 1, (255, 0, 0), 2)

                cv2.imshow('img', img)
                k = cv2.waitKey(30) & 0xff
                if k == 27: break

        except KeyboardInterrupt:
            pass

    return img_cache, pix_cache, euc_cache