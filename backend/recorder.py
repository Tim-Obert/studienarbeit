from enum import Enum
from rx.core.typing import Disposable
from camera import Camera
from frameserver import FrameServer
from videowriter import VideoWriter
import asyncio
from datetime import datetime
from typing import Tuple, Dict

class RecordingTrigger(Enum):
    MOTION = 0
    MANUAL = 1

class Recorder:

    def __init__(self, fs: FrameServer) -> None:
        self.__frameserver = fs
        self.__recording: Dict[str, ActiveRecording] = dict()

    async def capture(self, cam: Camera, trigger: RecordingTrigger, duration: int = 10):
        if cam.name in self.__recording:
            return

        self.start_capture(cam, trigger)
        await asyncio.sleep(duration)
        self.stop_capture(cam)        

    def start_capture(self, cam: Camera, trigger: RecordingTrigger, with_buffer: bool = False) -> Tuple[VideoWriter, Disposable]:
        if cam.name in self.__recording:
            return

        buffer = self.__frameserver.get_buffer(cam.name)
        writer = VideoWriter(self.__generate_name(cam, trigger))
        writer.open()
        if with_buffer:
            writer.write_frames(buffer.get_frames())
        subscription = buffer.get_observable().subscribe(on_next=lambda f: writer.write_frame(f))
        self.__recording[cam.name] = ActiveRecording(writer, subscription)

    def stop_capture(self, cam: Camera):
        if cam.name not in self.__recording:
            return
        self.__recording[cam.name].subscription.dispose()
        self.__recording[cam.name].writer.close()
        del self.__recording[cam.name]

    async def capture_while_motion(self, cam: Camera, trigger: RecordingTrigger, threshold: int):
        if cam.name in self.__recording:
            self.__recording[cam.name].last_motion = datetime.now()
            return

        self.start_capture(cam, trigger, True)
        while True:
            await asyncio.sleep(1)
            now = datetime.now()
            last_motion = self.__recording[cam.name].last_motion
            if last_motion is not None and (now - last_motion).seconds > threshold:
                break
        self.stop_capture(cam)

    def __generate_name(self, cam: Camera, trigger: RecordingTrigger) -> str:
        return "recordings/" + cam.name + "_" + str(datetime.utcnow()) + "_" + str(trigger) + ".mp4"

class ActiveRecording:
    def __init__(self, writer: VideoWriter, subscription: Disposable) -> None:
        self.writer = writer
        self.subscription = subscription
        self.last_motion = None