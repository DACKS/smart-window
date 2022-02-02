# Smart Window

# Installation

```
pip install flask
pip install flask_mqtt flask_socketio eventlet APScheduler flask_apscheduler requests pytest flask_swagger flask_swagger_ui
```

Set environment variables for development:

PowerShell: 
```
$env:FLASK_APP = "flaskr/__init__.py"
$env:FLASK_ENV = "development"
```

Linux:
```
export FLASK_APP="flaskr/__init__.py"
export FLASK_ENV=development
```

Prior to runnng the application, a MQTT broker must be running.
We recommend using the [Mosquitto MQTT Broker](https://mosquitto.org/download/)

# Running the application

First of all, make sure that the MQTT broker is running. The Mosquitto MQTT broker can be launched using this command:
```
mosquitto
```

If it's the first time you run the application, you would need to initialize the database. 
You can use this command whenever you want to reset to an empty database.
```
flask init-db
```

To start the application, simply use this command in a terminal.
```
flask run
```

# Testing the application

We used [pytest](https://docs.pytest.org/) for unit testing and integration testing.

Use this command to run the rests:
```
python -m pytest ./tests
```
or this one:
```
pytest ./tests
```



Install AsyncAPI
```npm install -g @asyncapi/generator```

Generate AsyncAPI documentation
```ag window.yml @asyncapi/html-template -o output```
