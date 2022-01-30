
import datetime
import json
import math
import random
from re import S
import requests
from .singleton_meta import SingletonMeta
from .status_api import StatusApi
from . import db

window_update_interval = 0.1
outside_stats_update_interval = 60.0
inside_stats_update_interval = 10.0
notifications_update_interval = 5.0

window_break_chance = 0.00001
humidity_threshold = 30

class CurrentStatistics:

    def __init__(self):
        self.temp_c = 0
        self.pressure = 0
        self.humidity = 0


class WindowStatus(metaclass=SingletonMeta):
    
    def __init__(self):
        self.accumulated_outside_update_time = 0.0
        self.accumulated_inside_update_time = 0.0
        self.accumulated_notifications_update_time = 0.0

        self.current_outside_stats = CurrentStatistics()
        self.current_inside_stats = CurrentStatistics()

        self.app = None

    def init_app(self, app):
        self.app = app

    def update(self):
        self.update_outside_stats()
        self.update_inside_stats()
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
        self.update_statistics_db(True, self.current_outside_stats)

    # https://stackoverflow.com/questions/67230458/get-date-obj-as-percentage-of-that-day-python
    def timedelta_percentage(self, input_datetime):
        TOTAL_DAY_SECS = 86400.0
        d = input_datetime - datetime.datetime.combine(input_datetime.date(), datetime.time())
        return d.total_seconds() / TOTAL_DAY_SECS

    def lerp(self, a, b, p):
        return a + (b - a) * p

    def update_inside_stats(self):

        day_perc = self.timedelta_percentage(datetime.datetime.now())
        self.current_inside_stats.temp_c = self.lerp(23.5, 25.5, math.sin(math.pi * day_perc))
        self.current_inside_stats.humidity = self.lerp(40.0, 30.0, math.sin(math.pi * day_perc))
        self.current_inside_stats.pressure = 1013.2

        self.accumulated_inside_update_time += window_update_interval
        if self.accumulated_inside_update_time < inside_stats_update_interval:
            return

        self.accumulated_inside_update_time -= inside_stats_update_interval

        status_api = StatusApi()
        status_api.publish_inside_stats(self.current_inside_stats)
        self.update_statistics_db(False, self.current_inside_stats)

    def update_statistics_db(self, isExterior, stats_object):

        isExteriorBit = 0
        if isExterior:
            isExteriorBit = 1

        with self.app.app_context():
            my_db = db.get_db()
            query_results = my_db.execute(f"SELECT * FROM swStatistics WHERE DATE('now')=DATE(createdAt) and isExterior={isExteriorBit}").fetchall()

            if len(query_results) <= 0:
                
                my_db.execute(f"INSERT INTO swStatistics (isExterior, minTemperature, maxTemperature, humidity, pressure) VALUES ({isExteriorBit}, {stats_object.temp_c}, {stats_object.temp_c}, {stats_object.humidity}, {stats_object.pressure})")
            
                query_results2 = my_db.execute(f"SELECT * FROM swStatistics WHERE isExterior = {isExteriorBit}").fetchall()
                for result in query_results2:
                    print(str(result["createdAt"]))

            else:

                result = query_results[0]
                minTemperature = min(result["minTemperature"], stats_object.temp_c)
                maxTemperature = max(result["maxTemperature"], stats_object.temp_c)
                humidity = stats_object.humidity
                pressure = stats_object.pressure

                my_db.execute(f"UPDATE swStatistics SET minTemperature = {minTemperature}, maxTemperature = {maxTemperature}, humidity={humidity}, pressure={pressure} WHERE DATE('now')=DATE(createdAt) and isExterior={isExteriorBit}")

            my_db.commit()


    def tried_break_window(self):
        chance = random.random()
        if chance < window_break_chance:
            return True

        return False
    
    def too_high_humidity(self):
        if self.current_inside_stats.humidity > humidity_threshold:
            return True
        return False

    def update_notifications(self):

        
        self.accumulated_notifications_update_time += window_update_interval
        if self.accumulated_notifications_update_time < notifications_update_interval:
            return

        self.accumulated_notifications_update_time -= notifications_update_interval

        notif_type = -1
        notification_content = ""

        if self.tried_break_window():
            notif_type = 0
            notification_content += "Someone is trying to break the window."

        if self.too_high_humidity():
            notif_type = 1
            notification_content += "Too high humidity, you should open the window."

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