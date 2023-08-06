import cv2
import numpy as np
from pathlib import Path, PosixPath
from jcopvision.exception import MediaToArrayError


class MediaReader:
    """
    An all around media reader built on top of opencv.

    === Example Usage ===
    media = MediaReader("video.mp4")
    for frame in media.read():
        # do something
    media.close()

    === Input ===
    source: "webcam" or str or int
        media source.
        - "webcam": access default webcam, or specify the webcam integer id as in opencv.
        - int: webcam integer id as in opencv
        - str: image or video filepath, or rtsp url
    """
    def __init__(self, source="webcam"):
        self.cam = None
        self.image = None
        self._parse_source(source)

    def _parse_source(self, source):
        source = 0 if source == "webcam" else source
        if isinstance(source, PosixPath):
            if not source.is_file():
                raise FileNotFoundError(f"Please check if '{source}' exists")
            if is_video(source):
                self.input_type = "video"
                self.cam = cv2.VideoCapture(source.as_posix())
            elif is_image(source):
                self.input_type = "image"
                self.image = cv2.imread(source.as_posix(), cv2.IMREAD_UNCHANGED)               
        elif isinstance(source, int) or source.startswith("rtsp://"):
            self.input_type = "camera"
            self.cam = cv2.VideoCapture(source)
        elif isinstance(source, str):
            self._parse_source(Path(source))
        else:
            raise Exception("File type not supported")

        if self.input_type == "image":
            h, w, c = self.image.shape
            self.aspect_ratio = w / h
            self.height = int(h)
            self.width = int(w) 
        elif self.input_type in ['video', "camera"]:
            self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.aspect_ratio = self.width / self.height
            self.frame_count = self.cam.get(cv2.CAP_PROP_FRAME_COUNT)
            self.frame_rate = self.cam.get(cv2.CAP_PROP_FPS)

    def read(self, rgb_output=True):
        if self.input_type == "image":
            return self.image
        else:
            def iter_func():
                while True:
                    cam_on, frame = self.cam.read()
                    if cam_on:
                        yield frame[..., ::-1] if rgb_output else frame
                    else:
                        break
            return iter_func()

    def capture(self):
        if self.input_type != "image":
            return next(iter(self.read()))

    def stream(self, transform=None):
        while True:
            cam_on, frame = self.cam.read()
            if cam_on:
                if transform is not None:
                    frame = transform(frame)
                success, frame = cv2.imencode(".jpg", frame)
                yield b'--frame\r\n' \
                      b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n'
            else:
                break

    def close(self):
        if self.input_type in ['video', "camera"]:
            self.cam.release()

    def to_array(self, mode="rgb"):
        if self.input_type == "video":
            frames = [frame for frame in self.read()]
            frames = np.array(frames).transpose(0, 3, 1, 2)
            if mode == "rgb":
                frames = frames[:, ::-1, :, :]
            return frames
        else:
            raise MediaToArrayError("Image / webcam stream could not be converted to array. Input should be a video.")


def is_video(fpath):
    return Path(fpath).suffix in [".mp4", ".avi"]


def is_image(fpath):
    return Path(fpath).suffix in [".bmp", ".dib", ".jpg", ".jpeg", ".jp2", ".jpe", ".png", ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tiff", ".tif"]