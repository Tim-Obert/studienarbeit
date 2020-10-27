from camera import Camera
from typing import List

class CameraRegistry:
    def __init__(self):
        self.__cameras = list()

    def get_cameras(self) -> List[Camera]:
        return self.__cameras

    def add_camera(self, cam: Camera):
        self.__cameras.append(cam)

    def get_camera_by_name(self, name) -> Camera:
        filtered = [cam for cam in self.__cameras if cam.name == name]
        if len(filtered) == 0:
            return None
        return filtered[0]

    
