
from threading import Thread

publisher_thread = None

def publish(mqtt_client):
    mqtt_client.publish('smart_window/temp', "1C")