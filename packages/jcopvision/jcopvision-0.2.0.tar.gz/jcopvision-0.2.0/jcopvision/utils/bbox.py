import numpy as np


def get_bbox_center(any_bbox):
    if any_bbox.ndim == 1:
        any_bbox = np.expand_dims(any_bbox, 0)
    assert any_bbox.shape[1] == 4

    xc = (any_bbox[:, 0] + any_bbox[:, 2]) / 2
    yc = (any_bbox[:, 1] + any_bbox[:, 3]) / 2
    center = np.concatenate([[xc, yc]], axis=1).T
    return center


def get_bbox_shape(any_bbox):
    if any_bbox.ndim == 1:
        any_bbox = np.expand_dims(any_bbox, 0)
    assert any_bbox.shape[1] == 4
    
    wbox = any_bbox[:, 2] - any_bbox[:, 0]
    hbox = any_bbox[:, 3] - any_bbox[:, 1]
    box_shape = np.concatenate([[wbox, hbox]], axis=1).T
    return box_shape


def normalize_bbox(frame, bbox):
    h, w, c = frame.shape
    norm_bbox = np.array(bbox) / [w, h, w, h]
    return norm_bbox


def denormalize_bbox(frame, norm_bbox):
    h, w, c = frame.shape
    bbox = np.array(norm_bbox) * [w, h, w, h]
    return bbox


def squarify_bbox(any_bbox, mult=1):
    centers = get_bbox_center(any_bbox)
    shapes = get_bbox_shape(any_bbox)
    shift = shapes.max(1, keepdims=True) * mult / 2
    any_bbox = np.concatenate([centers - shift, centers + shift], axis=1)
    return any_bbox


def expand_bbox(any_bbox, mult):
    centers = get_bbox_center(any_bbox)
    shapes = get_bbox_shape(any_bbox)
    shift = shapes * mult / 2
    any_bbox = np.concatenate([centers - shift, centers + shift], axis=1)
    return any_bbox


def shift_inside(norm_bbox):
    shapes = get_bbox_shape(norm_bbox)
    centers = get_bbox_center(norm_bbox)

    min_center = shapes / 2
    max_center = 1 - shapes / 2
    xshift = (min_center - centers).max(1).clip(0)
    yshift = (centers - max_center).max(1).clip(0)
    shift = np.concatenate([[xshift, yshift, xshift, yshift]], axis=1).T
    return norm_bbox + shift


def clip_bbox(norm_bbox):
    return np.array(norm_bbox).clip(0, 1)
