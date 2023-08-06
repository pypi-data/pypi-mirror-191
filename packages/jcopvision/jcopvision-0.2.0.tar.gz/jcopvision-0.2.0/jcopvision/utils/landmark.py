import numpy as np

def denormalize_landmark(frame, norm_landmarks):
    """
    frame: (H, W, C)
        image for the landmark detection
    norm_landmarks: (N, 2)
        landmark normalized coordinates (x, y)
    """
    h, w, c = frame.shape
    landmarks = np.array(norm_landmarks) * [w, h]
    return landmarks


def landmark2bbox(norm_landmarks):
    norm_bbox = np.concatenate([norm_landmarks.min(0), norm_landmarks.max(0)])
    return norm_bbox.reshape(1, 4)
