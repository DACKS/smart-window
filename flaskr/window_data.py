import json

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class WindowData(metaclass=Singleton):
    def __init__(self):
        with open("windows.json", "r") as f:
            w= json.load(f)
        self.name = w['name']
        self.openDirection = w['openDirection']
        self.openAngle = w['openAngle']
        self.integrity = w['integrity']
    
    def get_dict(self):
        return {
            'name': self.name,
            'openDirection': self.openDirection,
            'openAngle': self.openAngle,
            'integrity': self.integrity
        }


    def _update_json(self):
        with open("windows.json", "w") as f:
            x={"name":  self.name , "openDirection": self.openDirection,"openAngle": self.openAngle, "integrity": self.integrity}
            json.dump(x,f)

    def update_window_data(self, name, openDirection, openAngle, integrity):
        self.name = name
        self.openDirection = openDirection
        self.openAngle = openAngle
        self.integrity = integrity
        self._update_json()

