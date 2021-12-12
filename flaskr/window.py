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
        'SELECT w.id, w.name, w.openDirection, w.openAngle, w.integrity'
        ' FROM swindow w JOIN user u ON w.userID = u.id'
        ' ORDER BY w.createdAt DESC'
    ).fetchall()
    return render_template('window/index.html', windows=windows)


@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        error = None

        name = request.form['name']
        if not name:
            error = 'Title is required.'

        openDirection = request.form['name']

        openAngle = request.form['name']

        integrity = request.form['name']

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'INSERT INTO swindow (name, openDirection, openAngle, integrity, userID)'
                ' VALUES (?, ?, ?, ?, ?)',
                (name, openDirection, openAngle, integrity, g.user['id'])
            )
            my_db.commit()
            return redirect(url_for('window.index'))

    return render_template('window/create.html')


def get_window(id, check_user=True):
    window = db.get_db().execute(
        'SELECT w.id, w.name, w.openDirection, w.openAngle, w.integrity, w.userID'
        ' FROM swindow w JOIN user u ON w.userID = u.id'
        ' WHERE w.id = ?',
        (id,)
    ).fetchone()

    if window is None:
        abort(404, f"Window id {id} doesn't exist.")

    if check_user and window['userID'] != g.user['id']:
        abort(403)

    return window


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    window = get_window(id)

    if request.method == 'POST':
        error = None
        name = request.form['name']
        if not name:
            error = 'Name is required.'

        openDirection = request.form['name']
        if not openDirection:
            error = 'Open direction is not specified.'

        openAngle = request.form['name']
        if not openAngle:
            error = 'Open angle is not specified.'

        integrity = request.form['name']
        if not integrity:
            integrity = 'Integrity is required.'

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'UPDATE swindow SET'
                '   name = ?,'
                '   openDirection = ?,'
                '   openAngle = ?,'
                '   integrity = ?'
                ' WHERE id = ?',
                (name, id)
            )
            my_db.commit()
            return redirect(url_for('window.index'))

    return render_template('window/update.html', window=window)


@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    my_db = db.get_db()
    my_db.execute('DELETE FROM swindow WHERE id = ?', (id,))
    my_db.commit()
    return redirect(url_for('window.index'))