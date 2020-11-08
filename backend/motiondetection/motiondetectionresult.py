from camera import Camera


class MotionDetectionResult:

    def __init__(self, motion, accuracy, camera: Camera):
        self.motion = motion
        self.accuracy = accuracy
        self.camera = camera