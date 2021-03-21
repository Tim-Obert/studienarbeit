from datetime import datetime


class Camera:
    def __init__(self, name, url):
        self.id = 0
        self.name = name
        self.url = url
        self.last_motion: datetime = None
