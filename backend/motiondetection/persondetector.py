from motiondetection.motiondetector import MotionDetector
from motiondetection.motiondetectionresult import MotionDetectionResult
from models.camera import Camera
from framebuffer import FrameBuffer
import cv2

"""
Analyzes Video-Frames using Person-Detection Method
"""


class PersonDetector(MotionDetector):
    count = 0

    def __init__(self, *args) -> None:
        super().__init__(*args)

    async def _analyze(self, camera: Camera, buffer: FrameBuffer) -> MotionDetectionResult:
        frame = buffer.get_latest_packet()
        if frame == None:
            return MotionDetectionResult(False, 0, camera)
        img = cv2.cvtColor(frame.to_rgb().to_ndarray(), cv2.COLOR_BGR2RGB)

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        bounding_boxes, weights = hog.detectMultiScale(img, winStride=(8,8))
        if len(bounding_boxes) == 0:
            return MotionDetectionResult(False, 0, camera)    

        #boxes = []
        #for (x, y, w, h) in bounding_boxes:
        #    boxes.append((x,y,w,h))
	        #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.imwrite("./recordings/res" + str(self.count) + ".png", img)
        #self.count += 1
        return MotionDetectionResult(True, 50, camera, [[int(x),int(y),int(w),int(h)] for (x,y,w,h) in bounding_boxes])

