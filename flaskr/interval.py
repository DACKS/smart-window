import functools
from os import name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db
from . import auth

bp = Blueprint('interval', __name__)

@bp.route('/intervals/')
def index():
    my_db = db.get_db()
    intervals = my_db.execute(
        'SELECT *'
        ' FROM interval'
        ' ORDER BY createdAt DESC'
    ).fetchall()
    return render_template('interval/index.html', intervals=intervals)


@bp.route('/interval/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        error = None
        name = request.form['name']

        iStart = request.form['iStart']
        iStart = iStart.replace('T', ' ') + ':00'

        iEnd = request.form['iEnd']
        iEnd = iEnd.replace('T', ' ') + ':00'

        if not iStart or not iEnd:
            error = 'interval field missing'

        luminosity = request.form['luminosity']

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'INSERT INTO interval (name, iStart, iEnd, luminosity)'
                ' VALUES (?, ?, ?, ?)',
                (name, iStart, iEnd, luminosity)
            )
            my_db.commit()
            return redirect(url_for('interval.index'))

    return render_template('interval/create.html')


def get_interval(id, check_user=True):
    interval = db.get_db().execute(
        'SELECT *'
        ' FROM interval'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if interval is None:
        abort(404, f"Interval id {id} doesn't exist.")

    # if check_user and interval['userID'] != g.user['id']:
    #     abort(403)

    return interval


@bp.route('/interval/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    interval = get_interval(id)

    if request.method == 'POST':
        name = request.form['name']
        error = None

        iStart = request.form['iStart']        
        iEnd = request.form['iEnd']
        if not iStart or not iEnd:
            error = 'interval field missing'

        luminosity = request.form['luminosity']
        
        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'UPDATE interval SET'
                '   name = ?,'
                '   iStart = ?,'
                '   iEnd = ?,'
                '   luminosity = ?'
                ' WHERE id = ?',
                (name, iStart, iEnd, luminosity, id)
            )
            my_db.commit()
            return redirect(url_for('interval.index'))

    return render_template('interval/update.html', interval=interval)


@bp.route('/interval/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    my_db = db.get_db()
    my_db.execute('DELETE FROM interval WHERE id = ?', (id,))
    my_db.commit()
    return redirect(url_for('interval.index'))