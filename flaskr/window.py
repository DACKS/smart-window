import functools
from os import name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db
from . import auth

bp = Blueprint('window', __name__)

@bp.route('/')
def index():
    my_db = db.get_db()
    windows = my_db.execute(
        'SELECT w.id, w.name'
        ' FROM swindow w JOIN user u ON w.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('window/index.html', windows=windows)


@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'INSERT INTO swindow (name, user_id)'
                ' VALUES (?, ?)',
                (name, g.user['id'])
            )
            my_db.commit()
            return redirect(url_for('window.index'))

    return render_template('window/create.html')


def get_window(id, check_user=True):
    window = db.get_db().execute(
        'SELECT w.id, name, w.user_id'
        ' FROM swindow w JOIN user u ON w.user_id = u.id'
        ' WHERE w.id = ?',
        (id,)
    ).fetchone()

    if window is None:
        abort(404, f"Window id {id} doesn't exist.")

    if check_user and window['user_id'] != g.user['id']:
        abort(403)

    return window


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    window = get_window(id)

    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'UPDATE swindow SET name = ?'
                ' WHERE id = ?',
                (name, id)
            )
            my_db.commit()
            return redirect(url_for('window.index'))

    return render_template('window/update.html', window=window)


@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    get_window(id)
    my_db = db.get_db()
    my_db.execute('DELETE FROM swindow WHERE id = ?', (id,))
    my_db.commit()
    return redirect(url_for('window.index'))