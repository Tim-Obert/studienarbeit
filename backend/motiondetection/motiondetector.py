from abc import ABC, abstractmethod
from dbconnector import DBConnector
from framebuffer import FrameBuffer
from camera import Camera
from motiondetection.motiondetectionresult import MotionDetectionResult
from frameserver import FrameServer
import asyncio

class MotionDetector(ABC):
    _idle_time: int = 2

    on_result_handler = None

    def __init__(self, db: DBConnector, frameserver: FrameServer):
        self.db = db
        self.frameserver = frameserver
        pass

    async def run(self):
        while True:
            await self._on_before_analyze()

            for cam in self.db.get_cameras():
                res = await self._analyze(cam, self.frameserver.get_buffer(cam.name))
                await self._on_result(res)
                if self.on_result_handler is not None:
                    self.on_result_handler(res)
                    
            await self._on_after_analyze()
            await asyncio.sleep(self._idle_time)

    async def _on_before_analyze(self):
        pass

    @abstractmethod
    async def _analyze(self, camera: Camera, buffer: FrameBuffer) -> MotionDetectionResult:
        pass

    async def _on_result(self, result: MotionDetectionResult):
        pass

    async def _on_after_analyze(self):
        pass
