from abc import ABC, abstractmethod

from dbconnector import DBConnector
from framebuffer import FrameBuffer
from models.camera import Camera
from motiondetection.motiondetectionresult import MotionDetectionResult
from frameserver import FrameServer
import asyncio
import rx
from rx.core.typing import Observable

class MotionDetector(ABC):
    _idle_time: int = 0.5

    def __init__(self, db: DBConnector, frameserver: FrameServer):
        self.db = db
        self.frameserver = frameserver
        pass

    def run(self) -> Observable[MotionDetectionResult]:
        def analyze_observable(observer, scheduler):
            async def task(observer):
                while True:
                    await self._on_before_analyze()

                    for cam in self.db.get_cameras():
                        res = await self._analyze(cam, self.frameserver.get_buffer(cam.id))
                        await self._on_result(res)
                        observer.on_next(res)
                            
                    await self._on_after_analyze()
                    await asyncio.sleep(self._idle_time)
            return asyncio.create_task(task(observer))

        return rx.create(analyze_observable)

    async def _on_before_analyze(self):
        pass

    @abstractmethod
    async def _analyze(self, camera: Camera, buffer: FrameBuffer) -> MotionDetectionResult:
        pass

    async def _on_result(self, result: MotionDetectionResult):
        pass

    async def _on_after_analyze(self):
        pass
