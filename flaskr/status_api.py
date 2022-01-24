from tokenize import Single
from singleton_meta import SingletonMeta
import json

class StatusApi(metaclass=SingletonMeta):

    def __init__(self):
        self.mqtt_client = None

    def set_mqtt_client(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def publish_outside_stats(self, outside_stats):
        self.mqtt_client.publish('smart_window/outside_stats', str(json.dumps(outside_stats.__dict__)))