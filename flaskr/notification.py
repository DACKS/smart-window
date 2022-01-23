import functools
from os import abort, name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db
from . import auth

bp = Blueprint('notification', __name__)

@bp.route('/')
def index():
    my_db = db.get_db()
    notifications = my_db.execute(
        'SELECT *'
        ' FROM swNotification'
        ' ORDER BY createdAt DESC'
    ).fetchall()
    return render_template('notification/index.html', notifications=notifications)


@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        error = None
        content = request.form['content']

        if not content:
            error = 'Content is required.'

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'INSERT INTO swNotification (content, typeID)'
                ' VALUES (?, ?)',
                (content, 0)    # should be the id of an existing type
            )
            my_db.commit()
            return redirect(url_for('notification.index'))

    return render_template('notification/create.html')


def get_notification(id, check_user=True):
    notification = db.get_db().execute(
        'SELECT *'
        ' FROM swNotification'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if notification is None:
        abort(404, f"Notification id {id} doesn't exist.")

    if check_user and notification['userID'] != g.user['id']:
        abort(403)

    return notification


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    notification = get_notification(id)

    if request.method == 'POST':
        name = request.form['name']
        error = None

        iStart = request.form['iStart']        
        iEnd = request.form['iEnd']
        if not iStart or not iEnd:
            error = 'notification field missing'

        luminosity = request.form['luminosity']
        
        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'UPDATE swNotification SET content = ?'
                ' WHERE id = ?',
                (name, iStart, iEnd, luminosity, id)
            )
            my_db.commit()
            return redirect(url_for('notification.index'))

    return render_template('notification/update.html', notification=notification)


@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    my_db = db.get_db()
    my_db.execute('DELETE FROM swNotification WHERE id = ?', (id,))
    my_db.commit()
    return redirect(url_for('notification.index'))