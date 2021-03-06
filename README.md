# Smart Window

# About

This application is meant to be used for an IOT device which represents a smart window.
The key features of this application (selling points):

* Gives the user statistics about the inside and outside weather conditions
* Allows the user to set time intervals where the window would change the anount of light that it allows to go through
* Gives the user notifications about the events that may occur to the window/ house
* Allows multiple users to operate it.
* Detects when it needs to be opened/ closed based on the inside/ outside weather conditions.

# Installation

Prior to installation, you should have ```python 3``` and ```pip``` installed.

```
python3 -m pip install --user virtualenv
python3 -m venv venv
```

### Activate virtual environment
MacOS/Linux
```
source venv/bin/activate
```

Windows
```
.\venv\Scripts\activate
```

### Install required packages
```
python3 -m pip install -r requirements.txt
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
python3 -m flask init-db
```

To start the application, simply use this command in a terminal.
```
python3 -m flask run
```

# Testing the application

We used [pytest](https://docs.pytest.org/) for unit testing and integration testing.

Use this command to run the rests:
```
python3 -m pytest ./tests
```
or this one:
```
pytest ./tests
```

# Documentation

[Task analysis document](https://github.com/DACKS/smart-window/blob/main/Document_de_analiza_a_cerintelor_clientului.docx)

[How to use the application](https://github.com/DACKS/smart-window/blob/main/Document_utilizare_aplica%C8%9Bie.docx)

[Database diagram](https://github.com/DACKS/smart-window/blob/main/dbdiagram.pdf)

The data about the window is stored in a ```.json``` file, as the application is accountable for just one window, so there is no need for a table in the database.

For the HTTP endpoints documentation, you need to run the application, and access ```http://127.0.0.1:5000/api/docs```

We used AsyncAPI for the MQTT documentation. If you don't have AsyncAPI, you can install it by running the following command:
```
npm install -g @asyncapi/generator
```

The command used for generating an AsyncAPI documentation:
```
ag window.yml @asyncapi/html-template -o output
```
