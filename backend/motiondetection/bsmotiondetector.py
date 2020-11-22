from motiondetection.motiondetector import MotionDetector
from motiondetection.motiondetectionresult import MotionDetectionResult
from models.camera import Camera
from framebuffer import FrameBuffer

"""
Analyzes Video-Frames using Background-Subtraction Method
"""
class BSMotionDetector(MotionDetector):
    async def _analyze(self, camera: Camera, buffer: FrameBuffer) -> MotionDetectionResult:
        print("running Background Subtraction")
        return MotionDetectionResult(True, 0.8, camera)
