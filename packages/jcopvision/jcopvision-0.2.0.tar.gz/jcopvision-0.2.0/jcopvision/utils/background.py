import cv2
import numpy as np


def alpha_background(w, h):
    bg = np.kron([[0.95, 0.7] * (w // 20), [0.7, 0.95] * (w // 20)] * (h // 20), np.ones((3, 10, 10)))
    bg = bg.transpose(1, 2, 0)
    return cv2.resize(bg, (w, h))
