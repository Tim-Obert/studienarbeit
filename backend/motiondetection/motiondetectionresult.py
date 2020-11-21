from camera import Camera


class MotionDetectionResult:

    def __init__(self, motion, intensity, camera: Camera):
        self.motion = motion
        self.intensity = intensity
        self.camera = camera