import cv2
import numpy as np
from openni import openni2
from openni import _openni2 as c_api

fps = 30  # frames per second
width = 640  # Width of image
height = 480  # height of image


class OpenniClass:
    def __init__(self, file_pass):
        openni2.initialize(file_pass)
        dev = openni2.Device.open_any()

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.depth_stream = dev.create_depth_stream()
        dev.set_image_registration_mode(True)  # 彩色和深度图像对齐
        dev.set_depth_color_sync_enabled(True)
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                               resolutionX=width, resolutionY=height, fps=fps))
        self.depth_stream.start()

    def color_read(self):
        ret, frame = self.cap.read()
        # frame.shape = (height, width, 3)
        return frame

    def depth_read(self):
        frame = self.depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.ndarray((frame.height, frame.width), dtype=np.uint16, buffer=frame_data)
        img = cv2.flip(img, 1)
        return img

    def depth_read_range(self, min, max):
        img = self.depth_read()
        float_data = np.zeros(img.shape[:2], dtype=np.float64)
        out = np.zeros(img.shape[:2], dtype=np.uint8)
        img[img < min] = min
        img[img > max] = max
        img = img - min
        float_data = img.astype(np.float64)
        float_data = ((float_data - (max - min)) / (max - min)) * 255.0
        out = float_data.astype(np.uint8)
        return out

    def depth_read_format(self):
        img = self.depth_read()
        float_data = np.zeros(img.shape[:2], dtype=np.float64)
        out = np.zeros(img.shape[:2], dtype=np.uint8)
        max = np.max(img)
        min = np.min(img)
        img = img - min
        float_data = img.astype(np.float64)
        float_data = ((float_data - (max - min)) / (max - min)) * 255.0
        out = float_data.astype(np.uint8)
        return out


    @staticmethod
    def destroy():
        openni2.unload()
        cv2.destroyAllWindows()
