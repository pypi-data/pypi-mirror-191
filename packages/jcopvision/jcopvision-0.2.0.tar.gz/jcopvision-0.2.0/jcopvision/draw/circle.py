import cv2
from jcopvision.utils import denormalize_landmark, denormalize_landmark, denormalize_image, idx2color


def draw_circle(frame, pt, radius, color, thickness=1, is_normalized=True):
    '''
    Draw a circle


    === Input ===
    frame: array
        image / frame to be drawn

    pt: (int, int) or (float, float)
        location to draw the circle.
        If is_normalized is True, then the point will be rescaled back based on the frame size.

    color: (int, int, int)
        The circle color in BGR format

    thickness: int
        The bounding box and text thickness

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

    if is_normalized:
        pt = tuple(denormalize_landmark(frame, pt))

    cv2.circle(frame, pt, radius, color, thickness)
    return frame
