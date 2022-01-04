import functools
from os import name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db
from . import auth

bp = Blueprint('notificationType', __name__)

@bp.route('/')
def index():
    my_db = db.get_db()
    notificationTypes = my_db.execute(
        'SELECT *'
        ' FROM notificationType'
        ' ORDER BY createdAt DESC'
    ).fetchall()
    return render_template('notificationType/index.html', notificationTypes=notificationTypes)


@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = 'Description field missing'

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'INSERT INTO notificationType (description)'
                ' VALUES (?)',
                (description,)
            )
            my_db.commit()
            return redirect(url_for('notificationType.index'))

    return render_template('notificationType/create.html')


def get_notificationType(id):
    notificationType = db.get_db().execute(
        'SELECT *'
        ' FROM notificationType'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if notificationType is None:
        abort(404, f"NotificationType id {id} doesn't exist.")

    return notificationType


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    notificationType = get_notificationType(id)

    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = 'Description field missing'
        
        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'UPDATE notificationType SET description = ?'
                ' WHERE id = ?',
                (description, id)
            )
            my_db.commit()
            return redirect(url_for('notificationType.index'))

    return render_template('notificationType/update.html', notificationType=notificationType)


@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    my_db = db.get_db()
    my_db.execute('DELETE FROM notificationType WHERE id = ?', (id,))
    my_db.commit()
    return redirect(url_for('notificationType.index'))