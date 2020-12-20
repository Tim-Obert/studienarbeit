<<<<<<< HEAD
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


 # Settings
    def get_settings(self) -> Settings:
        data = self.__settings.get(doc_id=0)
        return Settings(data['frame_buffer_size'], data['video_path'])

    def update_settings(self, settings: Settings):
        self.__settings.update(settings.__dict__, doc_ids=[0])
=======
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
>>>>>>> origin/feature/backgroundSubtraction
