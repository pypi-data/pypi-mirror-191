import PIL.Image as PillowImage
from io import BytesIO

from ipywidgets import Image
from IPython.display import display, clear_output


class JupyterCameraStream:
    def __init__(self):
        self.image = Image(width=800)

    def __call__(self, frame, mode="bgr"):
        if mode == "bgr":
            frame = frame[..., ::-1]

        clear_output(wait=True)

        f = BytesIO()
        PillowImage.fromarray(frame).save(f, "jpeg")

        self.image.value = f.getvalue()
        display(self.image)

    def set_width(self, width):
        self.image = Image(width=width)
        print(f"width is updated to {width}")


jupyter_imshow = JupyterCameraStream()
