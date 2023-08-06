import cv2
import numpy as np
from jcopvision.utils import denormalize_image, idx2color


def draw_single_bbox(frame, bbox, color, label=None, conf=None, thickness=1, font=cv2.FONT_HERSHEY_SIMPLEX, fontsize=0.5, fontcolor=(0, 0, 0)):
    '''
    Draw a bounding box with its label

    === Example Usage ===
    - simple usage
    draw_bbox(frame, (x1, y1), (x2, y2), color=0)

    - When you have bounding boxes with labels and confidences
    for color, ((x1, y1, x2, y2), label, conf) in enumerate(zip(boxes, labels, confs)):
        draw_bbox(frame, (x1, y1), (x2, y2), color, label, conf)


    === Input ===
    frame: array
        image / frame to be drawn

    bbox: (int, int, int, int)
        4 integer representing (xmin, ymin, xmax, ymax)

    color: (int, int, int)
        The bounding box color in BGR format

    label: str
        A text or class label. It will be added to the inner top left of the bounding box

    conf: float
        The prediction confidence (0 to 1)

    thickness: int
        The bounding box and text thickness

    font: opencv's font
        The text font. Check for the available font in opencv

    fontsize: float
        The font scaling factor towards the font's base size

    fontcolor: (int, int, int)
        The text font color in BGR format

    is_normalized: bool
        True if using normalized coordinate


    === Return ===
    frame: array
        annotated image / frame
    '''
    frame = frame.copy()
    frame = denormalize_image(frame)

    if isinstance(color, int):
        color = idx2color(color)

    bbox = np.array(bbox).astype(int)
    pt1 = tuple(bbox[:2])
    pt2 = tuple(bbox[2:])

    cv2.rectangle(frame, pt1, pt2, color, thickness)

    text = ""
    if label is not None:
        text += label

    if conf is not None:
        text += f" [{conf*100:.1f}%]"

    if text != "":
        # Handle text size
        (w_text, h_text), baseline = cv2.getTextSize(text, font, fontsize, thickness)

        # Filled textbox
        pt1_box = pt1
        pt2_box = (pt1[0] + w_text + 2 * baseline, pt1[1] + h_text + 2 * baseline)
        cv2.rectangle(frame, pt1_box, pt2_box, color, cv2.FILLED)

        # Add text
        pt_text = (pt1[0] + baseline, pt1[1] + h_text + baseline - thickness)
        cv2.putText(frame, text, pt_text, font, fontsize, fontcolor, thickness)
    return frame
