import cv2
import numpy as np

from jcopvision.utils import normalize_image


def alpha_blending(source, source_mask, background, offset=(0, 0), resize_source=None, resize_bg=None):
    # Handle tipe data
    source = normalize_image(source)
    source_mask = normalize_image(source_mask)
    background = normalize_image(background)

    # Handle resizing
    if resize_source is not None:
        source = cv2.resize(source.copy(), resize_source)
        source_mask = cv2.resize(source_mask.copy(), resize_source)

    if resize_bg is not None:
        background = cv2.resize(background.copy(), resize_bg)

    # Handle dimensi mask
    if source_mask.ndim == 2:
        source_mask = source_mask[:, :, None]

    # Handle offset dan inisialisasi hasil composite
    hs, ws, _ = source_mask.shape
    hb, wb, _ = background.shape
    xs = ys = xb = yb = 0

    xoff, yoff = offset
    if xoff > 0:
        xs += xoff
    else:
        xb -= xoff

    if yoff > 0:
        ys += yoff
    else:
        yb -= yoff

    w = max(xs + ws, xb + wb) - min(xs, xb)
    h = max(ys + hs, yb + hb) - min(ys, yb)
    result = np.zeros((h, w, 3))

    # Compositing
    result[yb:yb+hb, xb:xb+wb, :] = background
    result[ys:ys+hs, xs:xs+ws, :] = source_mask * source + (1 - source_mask) * result[ys:ys+hs, xs:xs+ws, :]
    return result
