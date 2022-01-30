import functools
from os import name

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db
from . import auth

bp = Blueprint('statistics', __name__)

@bp.route('/')
def index():
    my_db = db.get_db()
    statisticsList = my_db.execute(
        'SELECT *'
        ' FROM swStatistics ss JOIN ('
        ' 	SELECT sw.id AS windowID, u.id AS userID'
        '	FROM swindow sw JOIN user u ON sw.userID = u.id'
        ' ) w ON ss.windowID = w.windowID'
        ' ORDER BY ss.createdAt DESC'
    ).fetchall()
    return render_template('statistics/index.html', statisticsList=statisticsList)


@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        error = None

        isExterior = request.form['isExterior']
        if not isExterior:
            error = "Must specify if the statistics are for the interior or the exterior"

        minTemperature = request.form['minTemperature']
        maxTemperature = request.form['maxTemperature']
        if not minTemperature or not maxTemperature:
            error = "Missing temperature informations"

        humidity = request.form['humidity']
        if not humidity:
            error = "Missing field - humidity"

        pressure = request.form['pressure']
        if not pressure:
            error = "Missing field - pressure"

        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'INSERT INTO swStatistics (windowID, isExterior, minTemperature, maxTemperature, humidity, pressure)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (g.swindow['id'], isExterior, minTemperature, maxTemperature, humidity, pressure)
            )
            my_db.commit()
            return redirect(url_for('statistics.index'))

    return render_template('statistics/create.html')


def get_statistics(id, check_user=True):
    statistics = db.get_db().execute(
        'SELECT *'
        ' FROM swStatistics ss JOIN ('
        ' 	SELECT sw.id AS windowID, u.id AS userID'
        '	FROM swindow sw JOIN user u ON sw.userID = u.id'
        ' ) w ON ss.windowID = w.windowID'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if statistics is None:
        abort(404, f"Interval id {id} doesn't exist.")

    if check_user and statistics['userID'] != g.user['id']:
        abort(403)

    return statistics


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    statistics = get_statistics(id)

    if request.method == 'POST':
        error = None

        isExterior = request.form['isExterior']
        if not isExterior:
            error = "Must specify if the statistics are for the interior or the exterior"

        minTemperature = request.form['minTemperature']
        maxTemperature = request.form['maxTemperature']
        if not minTemperature or not maxTemperature:
            error = "Missing temperature informations"

        humidity = request.form['humidity']
        if not humidity:
            error = "Missing field - humidity"

        pressure = request.form['pressure']
        if not pressure:
            error = "Missing field - pressure"
        
        if error is not None:
            flash(error)
        else:
            my_db = db.get_db()
            my_db.execute(
                'UPDATE swStatistics SET'
                '   isExterior = ?,'
                '   minTemperature = ?,'
                '   maxTemperature = ?,'
                '   humidity = ?,'
                '   pressure = ?'
                ' WHERE id = ?',
                (isExterior, minTemperature, maxTemperature, humidity, pressure, id)
            )
            my_db.commit()
            return redirect(url_for('statistics.index'))

    return render_template('statistics/update.html', statistics=statistics)


@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    my_db = db.get_db()
    my_db.execute('DELETE FROM swStatistics WHERE id = ?', (id,))
    my_db.commit()
    return redirect(url_for('statistics.index'))



def get_all_statistics(check_user=True):
    statistics = db.get_db().execute(
        'SELECT * from swStatistics'
    ).fetchone()


    my_db = db.get_db()
    statistics = my_db.execute(
        'SELECT *'
        ' FROM swStatistics'
        ' ORDER BY id'
    ).fetchall()

    return statistics

@bp.route('/afisare', methods=('GET', 'POST'))
@auth.login_required
def afisare():
    statistics2 = get_all_statistics()
    

    return render_template('statistics/afisare.html', statistics2=statistics2)