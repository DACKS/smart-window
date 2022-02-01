import json
import os
from flaskr.utils.singleton_meta import SingletonMeta
from pathlib import Path

class WindowData(metaclass=SingletonMeta):
    MAX_OPEN_ANGLE = 90
    JSON_PATH = os.path.join(os.path.dirname(__file__), 'windows.json')

    def __init__(self):
        self.alter_file_path(self.JSON_PATH)
        self.reload_json()

    def alter_file_path(self, new_file_path):
        self.JSON_PATH = new_file_path
        if not os.path.exists(self.JSON_PATH):
            myfile = Path(self.JSON_PATH)
            myfile.touch(exist_ok=True)
            self.update_window_data("", 0, 0, 100)
        
    def reload_json(self):
        with open(self.JSON_PATH, "r") as f:
            w = json.load(f)
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
        with open(self.JSON_PATH, "w") as f:
            x={"name":  self.name , "openDirection": self.openDirection,"openAngle": self.openAngle, "integrity": self.integrity}
            json.dump(x,f)

    def update_window_data(self, name=None, openDirection=None, openAngle=None, integrity=None):
        if name is not None: 
            self.name = name
        if openDirection is not None:
            self.openDirection = openDirection
        if openAngle is not None:
            self.openAngle = int(openAngle)
        if integrity is not None:
            self.integrity = int(integrity)

        self._update_json()

    def humidity_check(self, inside_humidity, outside_humidity):
        if abs(inside_humidity - outside_humidity) > self.openAngle and self.openAngle < self.MAX_OPEN_ANGLE:
            new_openAngle = min(self.MAX_OPEN_ANGLE, abs(inside_humidity - outside_humidity))
            diff = round(self.openAngle - new_openAngle)
            self.openAngle = new_openAngle
            if diff == 0:
                return None
            if diff > 0:
                return f"Inside and outside humidity difference too high, opening the window by {diff} degrees..."
            return f"Inside and outside humidity difference too high, closing the window by {-diff} degrees..."
        return None

        
            
        