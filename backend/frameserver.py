from camera import Camera
from framebuffer import FrameBuffer
import cv2 as cv
import asyncio
from aiortc.contrib.media import MediaPlayer

class FrameServer:

    __players = dict()
    __buffers = dict()
    frametime = 1/100

    def __init__(self):
        pass

    async def capture(self, cam: Camera):
        #vcap = cv.VideoCapture(cam.url)
        #while(1):
        #    print(cam.name)
        #    ret, frame = vcap.read()
        #    self.buff[cam.name] = frame
        #    await asyncio.sleep(self.frametime)
        player = MediaPlayer(cam['url'], options={"rtsp_transport": "tcp"})
        self.__buffers[cam['name']] = FrameBuffer(1000)
        self.__players[cam['name']] = player
        while(1):
            frame = await player.video.recv()
            audio = await player.audio.recv()
            self.__buffers[cam['name']].add(frame)
            await asyncio.sleep(self.frametime)

    def get_player(self, name: str) -> MediaPlayer:
        return self.__players[name]

    def get_buffer(self, name: str) -> FrameBuffer:
        return self.__buffers[name]
