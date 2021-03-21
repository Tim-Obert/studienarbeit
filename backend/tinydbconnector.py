from dbconnector import DBConnector
from tinydb import TinyDB, Query
from models.camera import Camera
from models.settings import Settings
from typing import List


class TinyDBConnector(DBConnector):
    def __init__(self, path: str) -> None:
        self.path = path
        self.__cameras = TinyDB(self.path).table('cameras')
        self.__settings = TinyDB(self.path).table('settings')

    def get_cameras(self) -> List[Camera]:
        cameras = []
        for data in self.__cameras.all():
            cam = Camera(data['name'], data['url'])
            cam.id = data['id']
            cameras.append(cam)
        return cameras

    def get_camera(self, id: int) -> Camera:
        data = self.__cameras.get(doc_id=id)
        cam = Camera(data['name'], data['url'])
        cam.id = id
        return cam

    def insert_camera(self, cam: Camera) -> int:
        return self.__cameras.insert(cam.__dict__)

    def update_camera(self, id: int, cam: Camera):
        self.__cameras.update(cam.__dict__, doc_ids=[id])

    def delete_camera(self, id: int):
        self.__cameras.remove(doc_ids=[id])

    # Settings
    def get_settings(self) -> Settings:
        data = self.__settings.get(doc_id=0)
        return Settings(data['frame_buffer_size'], data['video_path'])

    def update_settings(self, settings: Settings):
        self.__settings.update(settings.__dict__, doc_ids=[0])
