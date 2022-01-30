import functools
from os import name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from .window_data import WindowData
window = WindowData()

from . import db
from . import auth
import json

bp = Blueprint('window', __name__)

@bp.route('/')
def index():
    return render_template('window/index.html', window=window.get_dict())

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


