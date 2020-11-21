from enum import Enum
from camera import Camera
from frameserver import FrameServer
from videowriter import VideoWriter
import asyncio
import datetime

class RecordingTrigger(Enum):
    MOTION = 0
    MANUAL = 1

class Recorder:
    def __init__(self, fs: FrameServer) -> None:
        self.__frameserver = fs
        self.__recording = dict()

    async def start_capture(self, cam: Camera, trigger: RecordingTrigger):
        if cam.name in self.__recording:
            return
        self.__recording[cam.name] = True

        buffer = self.__frameserver.get_buffer(cam.name)
        writer = VideoWriter(self.__generate_name(cam, trigger))
        writer.open()
        writer.write_frames(buffer.get_frames())
        subscription = buffer.get_observable().subscribe(on_next=lambda f: writer.write_frame(f))
        await asyncio.sleep(10)
        subscription.dispose()
        writer.close()

        del self.__recording[cam.name]

    async def stop_capture(self):
        pass

    def __generate_name(self, cam: Camera, trigger: RecordingTrigger) -> str:
        return "recordings/" + cam.name + "_" + str(datetime.datetime.utcnow()) + "_" + str(trigger) + ".mp4"