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
```.venv\Scripts\activate.bat```

Set environment value for development: export ```FLASK_ENV=development```

CMD: set ```FLASK_ENV=development```

PowerShell: ```$env:FLASK_ENV = "development"```

```export FLASK_APP="flaskr"```
```export FLASK_ENV=development```

Initialize (or reinitialize) database:
```flask init-db```

Run
```flask run```