from concurrent.futures import thread
import tempfile
import pytest
import os
import sys

from __init__ import create_app
from storage import db
from storage.window_data import WindowData
from flaskr import WindowStatus, humidity_threshold

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

def authorize(client):
    client.post('api/auth/register', data={'username': 'username', 'password': 'password'})
    client.post('api/auth/login', data={'username': 'username', 'password': 'password'})

# =================== DATABASE =================

def test_db_connection(app):
    with app.app_context():
        result = False
        my_db = db.get_db()
        try:
            entry = my_db.execute('SELECT \'test\'').fetchone()

            if not entry:
                result = True
        except:
            result = True

        assert result == False

# =================== FUNCTIONALITY =================

def test_window_data(app):

    error = False

    try:

        window_data = WindowData()
        window_data.alter_file_path(os.path.join(os.path.dirname(__file__), 'testing.json'))
        window_data.reload_json()

        for direction in range(0, 3):
            for angle in range(10, 90, 5):
                name = 'cool window'
                integrity = 100

                window_data.update_window_data(name, direction, angle, integrity)
                new_data = window_data.get_dict()

                assert new_data['name'] == name
                assert new_data['openDirection'] == direction
                assert new_data['openAngle'] == angle
                assert new_data['integrity'] == integrity

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        error = True

    assert error == False

def test_humidity_check(app):

    window_data = WindowData()
    window_data.alter_file_path(os.path.join(os.path.dirname(__file__), 'testing.json'))
    window_data.reload_json()

    window_data.update_window_data("john", 0, 10, 100)
    
    res = window_data.humidity_check(40, 40)
    assert res == None

    res = window_data.humidity_check(40, 100)
    assert res != None

def test_window_status_outside(app):

    error = False

    try:

        window_status = WindowStatus()
        window_status.update_outside_stats()

        outside_stats = window_status.current_outside_stats

        assert outside_stats.humidity != None
        assert outside_stats.temp_c != None
        assert outside_stats.pressure != None

    except:

        error = True
    
    assert error == False

def test_window_status_inside(app):

    error = False

    try:

        window_status = WindowStatus()
        window_status.update_inside_stats()

        inside_stats = window_status.current_inside_stats

        assert inside_stats.humidity != None
        assert inside_stats.temp_c != None
        assert inside_stats.pressure != None

    except:

        error = True
    
    assert error == False

def test_tried_break_window(app):

    error = False

    try:

        window_status = WindowStatus()
        window_status.update_inside_stats()

        tried = window_status.tried_break_window()

        assert tried != None

    except:

        error = True
    
    assert error == False

def test_too_high_humidity(app):

    error = False

    try:

        window_status = WindowStatus()

        threshold = humidity_threshold

        for th in range(-100, 101):

            new_humidity = threshold + th
            window_status.current_inside_stats.humidity = new_humidity
            result = window_status.too_high_humidity()

            if new_humidity > threshold:
                assert result
            else:
                assert not result

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

        error = True
    
    assert error == False

# =================== HTTP API =================

