from dbconnector import DBConnector
from tinydb import TinyDB, Query
from camera import Camera
from typing import List

class TinyDBConnector(DBConnector):
    def __init__(self, path: str) -> None:
        self.path = path
        self.__cameras = TinyDB(self.path).table('cameras')

    def get_cameras(self) -> List[Camera]:
        return [Camera(data['name'], data['url']) for data in self.__cameras.all()]

    def get_camera(self, name: str) -> Camera:
        data = self.__cameras.search(Query().name == name)[0]
        return Camera(data['name'], data['url'])

    def insert_camera(self, cam: Camera):
        self.__cameras.insert(cam.__dict__)

    def update_camera(self, name: str, cam: Camera):
        self.delete_camera(name)
        self.insert_camera(cam)

    def delete_camera(self, name: str):
        self.__cameras.remove(Query().name == name)