import numpy as np


def normalize_image(frame):
    if frame.dtype == np.uint8:
        return frame / 255
    else:
        return frame


def denormalize_image(frame):
    if frame.dtype in [np.float32, np.float64]:
        return (frame * 255).astype(np.uint8)
    else:
        return frame


def crop_image(frame, bbox):
    return [frame[ymin: ymax, xmin: xmax, :] for xmin, ymin, xmax, ymax in bbox.astype(int)]
