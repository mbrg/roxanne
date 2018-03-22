import numpy as np
import cv2
from . import SOCCER, BASKETBALL


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


def frame(cap):
    # capture image
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detect soccer
    soccers = soccer_cascade.detectMultiScale(gray, 1.3, 5)
    has_soccer = False

    for x, y, w, h in soccers:
        has_soccer = True

        # bound soccer with a rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # detect soccer boundary
        soccer_boundary = gray[y:y + h, x:x + w]
        origin_x, origin_y, radius = detect_circle(soccer_boundary)



    return img, has_soccer


def video(ret_first_cap=False):

    img_cache = None

    with VideoCap(0) as vidcap:

        while True:
            try:
                img, has_soccer = frame(vidcap.cap)
                cv2.imshow('img', img)
                #cv2.waitKey(0)

                if ret_first_cap and has_soccer:
                    img_cache = img
                    break

            except KeyboardInterrupt:
                break

    return img_cache