import av
import imutils

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
    count = 0

    def __init__(self, *args) -> None:
        self.framestore = dict()
        super().__init__(*args)
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        self.initial_frame = None

    async def _analyze(self, camera: Camera, buffer: FrameBuffer) -> MotionDetectionResult:
        packet = buffer.get_latest_keyframe()
        if packet == None:
            return MotionDetectionResult(False, 0, camera)
        frames = packet.decode()
        vfs = [x for x in frames if isinstance(x, av.VideoFrame)]
        if len(vfs) == 0:
            return MotionDetectionResult(False, 0, camera)
        frame = vfs[0]

        img = cv2.cvtColor(frame.to_rgb().to_ndarray(), cv2.COLOR_BGR2RGB)
        img = imutils.resize(img, width=600)
        # Resize to have a width of 500px. Improves speed without sacrificing accuracy
        if self.initial_frame is None:
            self.initial_frame = img
            return MotionDetectionResult(False, 0, camera)

        dilated_frame = self.backSub.apply(img)

        # Find the contours of the dilated version of the thresholded image
        contours = cv2.findContours(dilated_frame.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        for contour in contours:
            boxes = []
            # If contour is smaller than the minimum specified area it does not represent
            #  significant motion and should thus be ignored
            if cv2.contourArea(contour) > 500:
                return MotionDetectionResult(True, 500, camera, boxes)
        return MotionDetectionResult(False, 0, camera)
