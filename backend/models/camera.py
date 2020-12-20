<<<<<<< HEAD:backend/models/camera.py
class Camera:
    def __init__(self, name, url):
        self.name = name
        self.url = url
=======
from datetime import datetime

class Camera:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.last_motion: datetime = None
>>>>>>> origin/feature/backgroundSubtraction:backend/camera.py
