import functools
from os import name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)


from . import db
from . import auth
import json

bp = Blueprint('window', __name__)

@bp.route('/window/')
def index():
    with open("windows.json", "r") as f:
        w= json.load(f)
       
        window= w["window"]
        
    return render_template('window/index.html', window=window)

@bp.route('/window/create', methods=('GET', 'POST'))
@auth.login_required
def create():
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
            with open("windows.json", "w") as f:

                x={"window": {"name":  name , "openDirection": openDirection,"openAngle":openAngle, "integrity":integrity}}
                json.dump(x,f)
            return redirect(url_for('window.index'))

    return render_template('window/create.html')


