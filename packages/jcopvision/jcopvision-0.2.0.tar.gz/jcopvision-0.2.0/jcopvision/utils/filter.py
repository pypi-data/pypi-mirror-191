import numpy as np


def filter_bbox_by_roi(boxes, pt1=(0, 0), pt2=(1, 1)):
    boxes = np.array(boxes)
    mask = (boxes > pt1 * 2) & (boxes < pt2 * 2)
    mask = mask.all(1)
    return boxes[mask]


def filter_bbox_by_area(boxes, area_range):
    boxes = np.array(boxes)

    pt1 = boxes[:, :2]
    pt2 = boxes[:, 2:]

    area = (pt2 - pt1).prod(1)
    mask = (area > area_range[0]) & (area < area_range[1])
    return boxes[mask]


def filter_bbox_by_score(boxes, scores, min_score=0.5):
    boxes = np.array(boxes)
    mask = scores > min_score
    return boxes[mask]


def nms(boxes, scores, max_iou=0.4):
    '''
    Vectorized implementation of Non-Max Suppression.

    === Input ===
    boxes: array (N, 4)
        bounding boxes

    scores: array (N,)
        prediction scores / confidences

    max_iou: float
        maximum IoU allowed


    === Return ===
    keep_id: array of int
        index of bbox to keep
    '''
    pt1 = boxes[:, :2]
    pt2 = boxes[:, 2:]

    area = (pt2 - pt1).prod(1)
    idx = scores.argsort()

    keep_id = []
    while len(idx) > 0:
        # Keep most confident prediction
        best, other = idx[-1], idx[:-1]
        keep_id.append(best)

        # Calculate Intersection Area with best
        intersect_pt1 = np.maximum(pt1[best], pt1[other])
        intersect_pt2 = np.minimum(pt2[best], pt2[other])
        intersection = np.maximum(1e-8, intersect_pt2 - intersect_pt1).prod(1)

        # Calculate Intersection over Union (IoU)
        IoU = intersection / (area[best] + area[other] - intersection)

        # Filter bbox based on IoU
        idx = idx[:-1]
        idx = idx[IoU <= max_iou]
    return keep_id
