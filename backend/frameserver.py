from models.camera import Camera
from framebuffer import FrameBuffer
import cv2 as cv
import asyncio
from aiortc.contrib.media import MediaPlayer
import typing
import av
import threading
import time

class FrameServer:

    #__players: typing.Dict[str, MediaPlayer] = dict()
    __buffers: typing.Dict[str, FrameBuffer] = dict()
    frametime = 1/4

    def __init__(self):
        pass

    async def capture(self, cam: Camera):
        #player = MediaPlayer(cam.url, options={"rtsp_transport": "tcp"})
        self.__buffers[cam.id] = FrameBuffer(30*10)
        #self.__players[cam.name] = player
        
        #while(1):
        #    frame = await player.video.recv()
        #    audio = await player.audio.recv()
        #    self.__buffers[cam.name].add(frame)
        #    await asyncio.sleep(self.frametime)

        capture_thread = threading.Thread(target= lambda x, y: self.__capture_thread(x, y), args=(cam, self.__buffers[cam.id]))
        capture_thread.start()

    def __capture_thread(self, cam: Camera, buffer: FrameBuffer):
        container = av.open(cam.url, mode="r", options={'rtsp_transport':'tcp'})
        last_pts = 0
        for packet in container.demux(container.streams.video[0]):
            if not isinstance(packet.pts, int):
                continue
            if packet.pts > last_pts:
                last_pts = packet.pts
                buffer.add(packet)

    #def get_player(self, id: int) -> MediaPlayer:
    #    return self.__players[id]

    def get_buffer(self, id: int) -> FrameBuffer:
        return self.__buffers[id]
