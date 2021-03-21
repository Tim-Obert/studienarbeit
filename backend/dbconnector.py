from abc import ABC, abstractmethod
from models.camera import Camera
from models.settings import Settings
from typing import List

class DBConnector(ABC):
    def __init__(self) -> None:
        pass

    #Cameras
    
    @abstractmethod
    def get_cameras(self) -> List[Camera]:
        pass

    @abstractmethod
    def get_camera(self, id: int) -> Camera:
        pass

    @abstractmethod
    def insert_camera(self, cam: Camera):
        pass 

    @abstractmethod
    def update_camera(self, id: int, cam: Camera):
        pass

    @abstractmethod
    def delete_camera(self, id: int):
        pass

    #Settings
    
    @abstractmethod
    def get_settings(self) -> Settings:
        pass

    @abstractmethod
    def update_settings(self, setting: Settings):
        pass
