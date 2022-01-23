# smart-window

# flaskr

To install the server's package:

```
cd flaskr
pip install -e .
pip install virtualenv
```

Create an environment:
```
python3 -m venv ./
```

Windows: 
```
python -m venv venv
```

Activate environment
macOS/Linux:
```
source venv/bin/activate
```

Windows:

Activate:

CMD: ```./venv/Scripts/activate.bat```

PowerShell: ```./venv/Scripts/Activate.ps1```

```
cd ../
```

```
pip install flask
```

'''
pip install flask_mqtt flask_socketio eventlet APScheduler flask_apscheduler
'''

Set environment value for development: export ```FLASK_ENV=development```

CMD: set ```FLASK_ENV=development```

PowerShell: 
```
$env:FLASK_APP = "flaskr/__init__.py"
$env:FLASK_ENV = "development"
```

```export FLASK_APP="flaskr"```
```export FLASK_ENV=development```

Initialize (or reinitialize) database:
```flask init-db```

Run
```flask run```