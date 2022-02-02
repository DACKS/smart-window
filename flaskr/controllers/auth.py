import functools
import json

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.storage import db

bp = Blueprint('auth', __name__, url_prefix='/auth')
bp_api = Blueprint('api-auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        my_db = db.get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                my_db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                my_db.commit()
            except:
                error = f"User {username} is already registered."
        else:
            return redirect(url_for('auth.login'))
        
        flash(error)
    return render_template('auth/register.html')

@bp_api.route('/register', methods=['POST'])
def api_register():
    
    my_db = db.get_db()
    try:
        username = request.json['username']
    except:
        return jsonify({'error': 'Username is required.'}), 400
    try:
        password = request.json['password']
    except:
        return jsonify({'error': 'Password is required.'}), 400

    try:
        my_db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        my_db.commit()
        return jsonify({'message': 'You have registered. Login with POST api/auth/login'}), 201
    except BaseException as err:
        return jsonify({'error': f"User {username} is already registered."}), 403
        


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        my_db = db.get_db()
        error = None
        user = my_db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp_api.route('/login', methods=['POST'])
def api_login():
    try:
        username = request.json['username']
    except:
        return jsonify({'error': 'Username is required.'}), 400
    try:
        password = request.json['password']
    except:
        return jsonify({'error': 'Password is required.'}), 400

    my_db = db.get_db()
    user = my_db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        return jsonify({'error': f"Incorrect username."}), 403
    elif not check_password_hash(user['password'], password):
        return jsonify({'error': f"Incorrect password."}), 403

    session.clear()
    session['user_id'] = user['id']
    return jsonify({'message': f" {user['username']} logged in with success"}), 200




@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp_api.route('/logout', methods=['GET', 'POST'])
def api_logout():
    session.clear()
    return jsonify({'message': 'Session cleared.'}), 200


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            if request.path.split('/')[1] == 'api':
                return jsonify({'message': 'you have to login with POST api/auth/login'}), 401 
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


