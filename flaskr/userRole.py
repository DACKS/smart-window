import functools
from os import abort, name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db
from . import auth

bp = Blueprint('userRole', __name__)

@bp.route('/')
def index():
    my_db = db.get_db()
    userRoles = my_db.execute(
        'SELECT *'
        ' FROM userRole'
        ' ORDER BY createdAt DESC'
    ).fetchall()
    return render_template('userRole/index.html', userRoles=userRoles)

@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        roleName = request.form['roleName']
        error = None

        if not roleName:
            error = 'roleName field missing'

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'INSERT INTO userRole (roleName)'
                ' VALUES (?)',
                (roleName,)
            )
            my_db.commit()
            return redirect(url_for('userRole.index'))

    return render_template('userRole/create.html')


def get_userRole(id):
    userRole = db.get_db().execute(
        'SELECT *'
        ' FROM userRole'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if userRole is None:
        abort(404, f"userRole id {id} doesn't exist.")

    return userRole


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    userRole = get_userRole(id)

    if request.method == 'POST':
        roleName = request.form['roleName']
        error = None

        if not roleName:
            error = 'roleName field missing'
        
        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'UPDATE userRole SET roleName = ?'
                ' WHERE id = ?',
                (roleName, id)
            )
            my_db.commit()
            return redirect(url_for('userRole.index'))

    return render_template('userRole/update.html', userRole=userRole)


@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    my_db = db.get_db()
    my_db.execute('DELETE FROM userRole WHERE id = ?', (id,))
    my_db.commit()
    return redirect(url_for('userRole.index'))