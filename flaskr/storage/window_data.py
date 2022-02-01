from datetime import datetime
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

    @staticmethod
    def check_luminosity(app, db): 
        with app.app_context():
            my_db = db.get_db()
            intervals = my_db.execute(
                'SELECT *'
                ' FROM interval'
                ' ORDER BY createdAt DESC'
            ).fetchall()
            intervals = [dict(interval) for interval in intervals]
            luminosity = None
            for interval in intervals:
                iStart = interval['iStart']
                iEnd = interval['iEnd']
                now = datetime.now()
                # if we are in the current interval
                if iStart < now < iEnd:
                    if luminosity is None:
                        luminosity = interval['luminosity']
                    else:
                        luminosity = min(luminosity, interval['luminosity'])
            
            # if we are not in any interval
            if luminosity is None:
                WindowData().luminosity = 100

            if luminosity != WindowData().luminosity:
                WindowData().update_window_data(luminosity=luminosity)


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
            self.luminosity = w['luminosity']

    def get_dict(self):
        return {
            'name': self.name,
            'openDirection': self.openDirection,
            'openAngle': self.openAngle,
            'integrity': self.integrity,
            'luminosity': self.luminosity
        }


    def _update_json(self):
        with open(self.JSON_PATH, "w") as f:
            x={"name":  self.name , "openDirection": self.openDirection,"openAngle": self.openAngle, "integrity": self.integrity, "luminosity": self.luminosity}
            json.dump(x,f)

    def update_window_data(self, name=None, openDirection=None, openAngle=None, integrity=None, luminosity=None):
        if name is not None: 
            self.name = name
        if openDirection is not None:
            self.openDirection = openDirection
        if openAngle is not None:
            self.openAngle = int(openAngle)
        if integrity is not None:
            self.integrity = int(integrity)
        if luminosity is not None:
            self.luminosity = int(luminosity)

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

        
            
        