import functools
from os import name
from signal import raise_signal

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
from flaskr.storage.window_data import WindowData
window = WindowData()

from flaskr.controllers import auth

bp = Blueprint('window', __name__)
bp_api = Blueprint('api-window', __name__, url_prefix='/api/window')

@bp.route('/')
@auth.login_required
def index():
    return render_template('window/index.html', window=window.get_dict())

@bp_api.route('/', methods=['GET'])
@auth.login_required
def api_window():
    return jsonify(window.get_dict())


@bp.route('/window/update', methods=('GET', 'POST'))
@auth.login_required
def update():
    if request.method == 'POST':
        error = None

        name = request.form['name']
        if not name:
            error = 'Title is required.'

        openDirection = request.form['opendirection']

        openAngle = request.form['openangle']

        if error is not None:
            flash(error)
        else:
            window.update_window_data(name, openDirection, openAngle)
            
            return redirect(url_for('window.index'))

    return render_template('window/update.html')

@bp_api.route('/update', methods=( 'PUT', ))
@auth.login_required
def api_update():

    try:
        name = request.json['name']
    except:
        return jsonify({'error': 'name is missing...'}), 400
    try:
        openDirection = request.json['openDirection']
        if openDirection != 'left' and openDirection != 'right':
            raise ValueError
    except ValueError:
        return jsonify({'error': 'openDirection must be left or right...'}), 400
    except:
        return jsonify({'error': 'openDirection is missing...'}), 400
    try:
        openAngle = request.json['openAngle']
        if type(openAngle) != float or openAngle < 0 or openAngle > 90:
            raise ValueError
    except ValueError:
        return jsonify({'error': 'openAngle should be a float between 0 and 90...'}), 400 
    except:
        return jsonify({'error': 'openAngle is missing...'}), 400

    window.update_window_data(name, openDirection, openAngle)
        
    return jsonify({'message': 'Window data has been updated with success!'}), 200


