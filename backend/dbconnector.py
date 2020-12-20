<<<<<<< HEAD
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
    def get_camera(self, name: str) -> Camera:
        pass

    @abstractmethod
    def insert_camera(self, cam: Camera):
        pass 

    @abstractmethod
    def update_camera(self, name: str, cam: Camera):
        pass

    @abstractmethod
    def delete_camera(self, name: str):
        pass

    #Settings
    
    @abstractmethod
    def get_settings(self) -> Settings:
        pass

    @abstractmethod
    def update_settings(self, setting: Settings):
        pass
=======
from abc import ABC, abstractmethod
from camera import Camera
from typing import List

class DBConnector(ABC):
    def __init__(self) -> None:
        pass

    #Cameras
    
    @abstractmethod
    def get_cameras(self) -> List[Camera]:
        pass

    @abstractmethod
    def get_camera(self, name: str) -> Camera:
        pass

    @abstractmethod
    def insert_camera(self, cam: Camera):
        pass 

    @abstractmethod
    def update_camera(self, name: str, cam: Camera):
        pass

    @abstractmethod
    def delete_camera(self, name: str):
        pass
>>>>>>> origin/feature/backgroundSubtraction
