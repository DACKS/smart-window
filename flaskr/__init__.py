from ast import Param
import os
from flaskr.storage import db
from flaskr.controllers import auth
from flaskr.controllers import userRole
from flaskr.controllers import interval
from flaskr.controllers import notification
from flaskr.controllers import notificationType
from flaskr.controllers import statistics
from flaskr.controllers import window as win
from flask import Flask
from flask_mqtt import Mqtt
from flask_apscheduler import APScheduler
from flask_swagger_ui import get_swaggerui_blueprint
from flaskr.window_status import *
from flaskr.status_api import StatusApi

def create_app(testing=False, db_path=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if db_path is None:
        db_path = os.path.join(app.instance_path, 'db.sqlite')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=db_path,
        MQTT_BROKER_URL='localhost',
        MQTT_BROKER_PORT=1883,
        MQTT_USERNAME='',
        MQTT_PASSWORD='',
        MQTT_KEEPALIVE=5,
        MQTT_TLS_ENABLED = False
    )

    mqtt = Mqtt()

    if testing:
        app.config['TESTING'] = True

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config = { 'title': "Smart Window" }
    )

    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(auth.bp)
    app.register_blueprint(auth.bp_api)
    app.register_blueprint(interval.bp)
    app.register_blueprint(interval.bp_api)
    app.register_blueprint(win.bp)
    app.register_blueprint(win.bp_api)
    app.register_blueprint(userRole.bp)
    app.register_blueprint(notification.bp)
    app.register_blueprint(notification.bp_api)
    app.register_blueprint(notificationType.bp)
    app.register_blueprint(statistics.bp)
    app.register_blueprint(statistics.bp_api)

    app.add_url_rule('/', endpoint='index')

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    mqtt.init_app(app)

    status_api = StatusApi()
    status_api.set_mqtt_client(mqtt)

    window = WindowStatus()
    window.init_app(app)

    scheduler.add_job('window_update', window.update, args=[], trigger="interval", seconds=window_update_interval)

    return app
    