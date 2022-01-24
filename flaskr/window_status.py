import imp
import json
import requests
from singleton_meta import SingletonMeta
from status_api import StatusApi

window_update_interval = 0.1
outside_stats_update_interval = 60.0

class CurrentStatistics:

    def __init__(self):
        self.temp_c = 0
        self.pressure = 0
        self.humidity = 0

class WindowStatus(metaclass=SingletonMeta):
    
    def __init__(self):
        self.accumulated_outside_update_time = 0.0
        self.current_outside_stats = CurrentStatistics()

    def update(self):
        self.update_outside_stats()

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