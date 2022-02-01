from tokenize import Single
from flaskr.utils.singleton_meta import SingletonMeta
import json

class StatusApi(metaclass=SingletonMeta):

    def __init__(self):
        self.mqtt_client = None

    def set_mqtt_client(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def publish_outside_stats(self, outside_stats):
        self.mqtt_client.publish('smart_window/outside_stats', str(json.dumps(outside_stats.__dict__)))

    def publish_inside_stats(self, inside_stats):
        self.mqtt_client.publish('smart_window/inside_stats', str(json.dumps(inside_stats.__dict__)))

    def publish_notification(self, notification_description):
        self.mqtt_client.publish("smart_window/notifications", notification_description)