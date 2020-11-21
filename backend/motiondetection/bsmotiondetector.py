from motiondetection.motiondetector import MotionDetector
from motiondetection.motiondetectionresult import MotionDetectionResult
from camera import Camera
from framebuffer import FrameBuffer
import cv2

"""
Analyzes Video-Frames using Background-Subtraction Method
"""
class BSMotionDetector(MotionDetector):
    def __init__(self, *args) -> None:
        self.framestore = dict()
        super().__init__(*args)

    
    async def _analyze(self, camera: Camera, buffer: FrameBuffer) -> MotionDetectionResult:
        frame = buffer.get_latest_frame()
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

        #cv2.imwrite('/mnt/c/Users/Hannes/Desktop/frame.jpg', diff) 
        return MotionDetectionResult(white > 20, white, camera)

