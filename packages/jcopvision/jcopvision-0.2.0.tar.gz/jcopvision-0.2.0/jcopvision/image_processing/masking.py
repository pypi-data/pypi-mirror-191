import cv2
import numpy as np

from jcopvision.io import create_sized_window, MediaReader, key_pressed
from jcopvision.image_processing.blending import alpha_blending
from jcopvision.utils import alpha_background


class ColorMaskSampler:
    def __init__(self, image_path, margin=10, app_height=500, window_name="Press `q` to quit | Press `r` to reset"):
        self.media = MediaReader(image_path)
        self.window_name = window_name
        self.app_height = app_height
        self.margin = margin

        self.mask = None
        self.image = None
        self.clicked_pixels = None
        self.result = None
        self.reset()

    def run(self):
        create_sized_window(self.app_height, self.media.aspect_ratio, self.window_name)
        cv2.setMouseCallback(self.window_name, self._sample)

        while True:
            if key_pressed("r"):
                self.reset()
            elif key_pressed("q"):
                break
            else:
                masked_image = alpha_blending(self.alpha_bg, self.mask, self.image)
                cv2.imshow(self.window_name, masked_image)

        cv2.destroyAllWindows()
        return self.result

    def reset(self):
        self.image = self.media.read()
        self.clicked_pixels = []
        self.result = ()

        h, w, c = self.image.shape
        self.mask = np.zeros((h, w, 1), dtype=np.uint8)
        self.alpha_bg = alpha_background(w, h)

    def _sample(self, action, x, y, flags, userdata):
        if action == cv2.EVENT_LBUTTONUP:
            self.clicked_pixels.append(self.image[y, x, :].astype(int))
            pmin = np.min(self.clicked_pixels, 0) - self.margin
            pmax = np.max(self.clicked_pixels, 0) + self.margin
            self.result = (pmin.clip(0, 255), pmax.clip(0, 255))
            self.mask = cv2.inRange(self.image, *self.result)



