from motiondetection.motiondetector import MotionDetector
from motiondetection.motiondetectionresult import MotionDetectionResult
from models.camera import Camera
from framebuffer import FrameBuffer
import cv2
import asyncio

"""
Analyzes Video-Frames using Background-Subtraction Method
"""
class BSMotionDetector(MotionDetector):
    def __init__(self, *args) -> None:
        self.framestore = dict()
        super().__init__(*args)

    
    async def _analyze(self, camera: Camera, buffer: FrameBuffer) -> MotionDetectionResult:
        await asyncio.sleep(10)
        return MotionDetectionResult(True, 100, camera, [])
        frame = buffer.get_latest_packet()
        if frame == None:
            return MotionDetectionResult(False, 0, camera)
        img = cv2.cvtColor(frame.to_rgb().to_ndarray(), cv2.COLOR_BGR2GRAY)
        if camera.name not in self.framestore:
            self.framestore[camera.name] = img
            return MotionDetectionResult(False, 0, camera)

        last = self.framestore[camera.name]
        self.framestore[camera.name] = img
        
        diff = cv2.subtract(img, last)
        ret, thresh = cv2.threshold(diff, 120, 255, cv2.THRESH_BINARY)
        white = cv2.countNonZero(thresh) # alternative: mean()

        boxes = []
        contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            # Find bounding rectangles
            x,y,w,h = cv2.boundingRect(contour)
            boxes.append([x,y,w,h])

        return MotionDetectionResult(white > 20, white, camera, boxes)

