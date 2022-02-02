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

# Documentation

[Task analysis document](https://github.com/DACKS/smart-window/blob/main/Document_de_analiza_a_cerintelor_clientului.pdf)

[How to use the application](https://github.com/DACKS/smart-window/blob/main/Document_utilizare_aplica%C8%9Bie.pdf)

[Database diagram](https://github.com/DACKS/smart-window/blob/main/dbdiagram.pdf)

For the HTTP endpoints documentation, you need to run the application, and access ```http://127.0.0.1:5000/api/docs```

We used AsyncAPI for the MQTT documentation. If you don't have AsyncAPI, you can install it by running the following command:
```
npm install -g @asyncapi/generator
```

The command used for generating an AsyncAPI documentation:
```
ag window.yml @asyncapi/html-template -o output
```
