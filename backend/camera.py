import json
class Camera:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def to_JSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
