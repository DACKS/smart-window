import imp
import json
import random
import requests
from singleton_meta import SingletonMeta
from status_api import StatusApi

import db

window_update_interval = 0.1
outside_stats_update_interval = 60.0

window_break_chance = 0.00001

class CurrentStatistics:

    def __init__(self):
        self.temp_c = 0
        self.pressure = 0
        self.humidity = 0

class WindowStatus(metaclass=SingletonMeta):
    
    def __init__(self):
        self.accumulated_outside_update_time = 0.0
        self.current_outside_stats = CurrentStatistics()
        self.app = None

    def init_app(self, app):
        self.app = app

    def update(self):
        self.update_outside_stats()
        self.update_notifications()

    def update_outside_stats(self):
        self.accumulated_outside_update_time += window_update_interval
        if self.accumulated_outside_update_time < outside_stats_update_interval:
            return

        self.accumulated_outside_update_time -= outside_stats_update_interval

        r = requests.get('http://api.weatherapi.com/v1/current.json?key=69a7e80c7e0641c3a84112121222401&q=Bucharest&aqi=no')
        if r.status_code != 200:
            return

        content = r.content
        json_data = json.loads(content)

        if "current" not in json_data:
            return
        current_object = json_data["current"]

        if "temp_c" not in current_object:
            return
        self.current_outside_stats.temp_c = current_object["temp_c"]

        if "pressure_mb" not in current_object:
            return
        self.current_outside_stats.pressure = current_object["pressure_mb"]

        if "humidity" not in current_object:
            return
        self.current_outside_stats.pressure = current_object["humidity"]

        status_api = StatusApi()
        status_api.publish_outside_stats(self.current_outside_stats)
        self.update_statistics_db()

    def update_statistics_db(self):

        with self.app.app_context():
            my_db = db.get_db()
            query_results = my_db.execute("SELECT * FROM swStatistics WHERE DATE('now')=DATE(createdAt) and isExterior=1").fetchall()

            if len(query_results) <= 0:
                
                my_db.execute(f"INSERT INTO swStatistics (isExterior, minTemperature, maxTemperature, humidity, pressure) VALUES (1, {self.current_outside_stats.temp_c}, {self.current_outside_stats.temp_c}, {self.current_outside_stats.humidity}, {self.current_outside_stats.pressure})")
            
                query_results2 = my_db.execute("SELECT * FROM swStatistics WHERE isExterior = 1").fetchall()
                for result in query_results2:
                    print(str(result["createdAt"]))

            else:

                result = query_results[0]
                minTemperature = min(result["minTemperature"], self.current_outside_stats.temp_c)
                maxTemperature = max(result["maxTemperature"], self.current_outside_stats.temp_c)
                humidity = self.current_outside_stats.humidity
                pressure = self.current_outside_stats.pressure

                my_db.execute(f"UPDATE swStatistics SET minTemperature = {minTemperature}, maxTemperature = {maxTemperature}, humidity={humidity}, pressure={pressure} WHERE DATE('now')=DATE(createdAt) and isExterior=1")

            my_db.commit()


    def tried_break_window(self):
        chance = random.random()
        if chance < window_break_chance:
            return True

        return False

    def update_notifications(self):

        notif_type = -1
        notification_content = ""

        if self.tried_break_window():
            notif_type = 0
            notification_content = "Someone is trying to break the window."

        if notif_type == -1:
            return

        with self.app.app_context():
            my_db = db.get_db()
            notification_descs = my_db.execute(f"SELECT * FROM notificationType n WHERE n.id = {notif_type}").fetchall()
            
            if len(notification_descs) > 0:

                status_api = StatusApi()
                status_api.publish_notification(notification_content)

                my_db.execute(f"INSERT INTO swNotification (content, typeID, createdAt) VALUES ('{notification_content}', {notif_type}, CURRENT_TIMESTAMP)")
                my_db.commit()