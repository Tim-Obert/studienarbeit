from models.camera import Camera


class MotionDetectionResult:

    def __init__(self, motion, intensity, camera: Camera, boxes=[]):
        self.motion = motion
        self.intensity = intensity
        self.camera = camera
        self.boxes = boxes  # [x, y, w, h]
