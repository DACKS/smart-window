import functools
from os import name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
from ..storage.window_data import WindowData
window = WindowData()

from . import auth

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
       

        integrity = request.form['integrity']

        if error is not None:
            flash(error)
        else:
            window.update_window_data(name, openDirection, openAngle, integrity)
            
            return redirect(url_for('window.index'))

    return render_template('window/update.html')


