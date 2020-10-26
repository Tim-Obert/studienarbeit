from camera import Camera
import cv2 as cv
from base64 import b64encode
import asyncio

class FrameServer:

    buff = dict()
    frametime = 1/30

    def __init__(self):
        pass

    async def capture(self, cam: Camera):
        vcap = cv.VideoCapture(cam.url)
        while(1):
            print(cam.name)
            ret, frame = vcap.read()
            self.buff[cam.name] = frame
            await asyncio.sleep(self.frametime)

    def get_frame_jpeg(self, name: str):
        retval, buf	= cv.imencode('.jpeg', self.buff[name])
        base64 = str(b64encode(buf), "utf-8")
        return base64