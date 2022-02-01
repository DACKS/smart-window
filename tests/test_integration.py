from concurrent.futures import thread
import tempfile
import pytest
import os
import sys
import json
from datetime import date, datetime

from flaskr.__init__ import create_app
from flaskr.storage import db
from flaskr.storage.window_data import WindowData
from flaskr import WindowStatus, humidity_threshold

from flaskr.controllers.interval import DATE_FORMAT

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(testing=True, db_path=db_path)

    with app.app_context():
        db.close_db()
        db.init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.mark.integtest
def test_integration(app, client):
    with app.app_context():

        # Register
        response = client.post('api/auth/register', json={'username': 'test_username', 'password': 'test_password'})
        assert response.status_code == 200

        # Login
        response = client.post('api/auth/login', json={'username': 'test_username', 'password': 'test_password'})
        assert response.status_code == 200

        # Get statistics
        response = client.get('api/statistics/')
        assert response.status_code == 200

        # Get notifications
        responsse = client.get('api/notifications/')
        assert response.status_code == 200

        # Get window data
        reponse = client.get('api/window/')
        assert response.status_code == 200

        # Update window data
        test_window = {
            'name': 'test_name',
            'openDirection': 'left',
            'openAngle': 10.2
        }
        response = client.post('api/window/update', json=test_window)
        assert response.status_code == 200

        # Get intervals
        respoonse = client.get('api/intervals/')
        assert response.status_code == 200

        # Create an interval
        test_interval = {
            "name": "test_interval",
            "iStart": "2022-01-10 02:02:00",
            "iEnd": "2022-01-10 02:10:00",
            "luminosity": 10
        }
        response = client.post('api/intervals/create', json=test_interval)
        assert response.status_code == 200

        # Update an interval
        response = client.get('api/intervals/')
        id = json.loads(response.data)[0]['id']
        response = client.post(f'api/intervals/{id}/update', json=test_interval)
        assert response.status_code == 200

        # Delete an interval
        response = client.get(f'api/intervals/{id}/delete')
        assert response.status_code == 200

        # Logout
        response = client.get(f'api/auth/logout')
        assert response.status_code == 200