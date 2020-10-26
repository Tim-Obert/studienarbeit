class CameraRegistry:
    def __init__(self):
        self.__cameras = list()

    def get_cameras(self):
        return self.__cameras

    def add_camera(self, cam):
        self.__cameras.append(cam)

    
