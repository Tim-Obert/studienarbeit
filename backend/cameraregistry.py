from camera import Camera
from typing import List
from tinydb import TinyDB, Query

class CameraRegistry:
    def __init__(self):
        self.__cameras = TinyDB('data/db.json').table('cameras')

    def get_cameras(self) -> List[Camera]:
        return self.__cameras.all()

    def add_camera(self, cam: Camera):
        self.__cameras.insert(cam.to_JSON())

    def get_camera_by_name(self, name) -> Camera:
        return self.__cameras.search(Query().name == name)

    def delete_camera(self, name):
        self.__cameras.remove(Query().name == name)    

    
