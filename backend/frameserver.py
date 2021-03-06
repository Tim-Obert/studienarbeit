from models.camera import Camera
from framebuffer import FrameBuffer
import cv2 as cv
import asyncio
from aiortc.contrib.media import MediaPlayer
import typing

class FrameServer:

    __players: typing.Dict[str, MediaPlayer] = dict()
    __buffers: typing.Dict[str, FrameBuffer] = dict()
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
        player = MediaPlayer(cam.url, options={"rtsp_transport": "tcp"})
        self.__buffers[cam.id] = FrameBuffer(100)
        self.__players[cam.id] = player
        while(1):
            frame = await player.video.recv()
            audio = await player.audio.recv()
            self.__buffers[cam.id].add(frame)
            await asyncio.sleep(self.frametime)

    def get_player(self, id: int) -> MediaPlayer:
        return self.__players[id]

    def get_buffer(self, id: int) -> FrameBuffer:
        return self.__buffers[id]
