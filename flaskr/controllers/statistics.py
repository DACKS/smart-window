import functools
from os import name
import statistics
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from flaskr.storage import db
from flaskr.controllers import auth

bp = Blueprint('statistics', __name__, url_prefix='/statistics')
bp_api = Blueprint('api-statistics', __name__, url_prefix='/api/statistics')


@bp.route('/', methods=('GET',))
@auth.login_required
def index():
    my_db = db.get_db()
    stats = my_db.execute(
        'SELECT *'
        ' FROM swStatistics'
        ' ORDER BY createdAt DESC'
    ).fetchall()
    stats = [dict(row) for row in stats]
    for stat in stats:
        stat['isExterior'] = 'Exterior' if stat['isExterior'] else 'Interior'
        stat['minTemperature'] = round(stat['minTemperature'], 2)
        stat['maxTemperature'] = round(stat['maxTemperature'], 2)
        stat['humidity'] = round(stat['humidity'], 2)
        stat['pressure'] = round(stat['pressure'], 2)
    return render_template('statistics/index.html', statistics=stats, stat_length=len(stats))

@bp_api.route('/', methods=('GET',))
@auth.login_required
def api_index():
    try:
        my_db = db.get_db()
        stats = my_db.execute(
            'SELECT *'
            ' FROM swStatistics'
            ' ORDER BY createdAt DESC'
        ).fetchall()
        stats = [dict(row) for row in stats]
        for stat in stats:
            stat['minTemperature'] = round(stat['minTemperature'], 2)
            stat['maxTemperature'] = round(stat['maxTemperature'], 2)
            stat['humidity'] = round(stat['humidity'], 2)
            stat['pressure'] = round(stat['pressure'], 2)
        return json.dumps(stats, default=str), 200
    except:
        return jsonify({'error': 'An error occured related to database...'}), 500

# @bp.route('/create', methods=('POST',))
# @auth.login_required
# def create():
#     if request.method == 'POST':
#         error = None

#         isExterior = request.form['isExterior']
#         if not isExterior:
#             error = "Must specify if the statistics are for the interior or the exterior"

#         minTemperature = request.form['minTemperature']
#         maxTemperature = request.form['maxTemperature']
#         if not minTemperature or not maxTemperature:
#             error = "Missing temperature informations"

#         humidity = request.form['humidity']
#         if not humidity:
#             error = "Missing field - humidity"

#         pressure = request.form['pressure']
#         if not pressure:
#             error = "Missing field - pressure"

#         if error is not None:
#             flash(error)
#         else:
#             my_db = db.get_db()
#             my_db.execute(
#                 'INSERT INTO swStatistics (windowID, isExterior, minTemperature, maxTemperature, humidity, pressure)'
#                 ' VALUES (?, ?, ?, ?, ?, ?)',
#                 (g.swindow['id'], isExterior, minTemperature, maxTemperature, humidity, pressure)
#             )
#             my_db.commit()
#             return redirect(url_for('statistics.index'))

#     return render_template('statistics/create.html')


# def get_statistics(id, check_user=True):
#     statistics = db.get_db().execute(
#         'SELECT *'
#         ' FROM swStatistics ss JOIN ('
#         ' 	SELECT sw.id AS windowID, u.id AS userID'
#         '	FROM swindow sw JOIN user u ON sw.userID = u.id'
#         ' ) w ON ss.windowID = w.windowID'
#         ' WHERE id = ?',
#         (id,)
#     ).fetchone()

#     if statistics is None:
#         abort(404, f"Interval id {id} doesn't exist.")

#     if check_user and statistics['userID'] != g.user['id']:
#         abort(403)

#     return statistics


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @auth.login_required
# def update(id):
#     statistics = get_statistics(id)

#     if request.method == 'POST':
#         error = None

#         isExterior = request.form['isExterior']
#         if not isExterior:
#             error = "Must specify if the statistics are for the interior or the exterior"

#         minTemperature = request.form['minTemperature']
#         maxTemperature = request.form['maxTemperature']
#         if not minTemperature or not maxTemperature:
#             error = "Missing temperature informations"

#         humidity = request.form['humidity']
#         if not humidity:
#             error = "Missing field - humidity"

#         pressure = request.form['pressure']
#         if not pressure:
#             error = "Missing field - pressure"
        
#         if error is not None:
#             flash(error)
#         else:
#             my_db = db.get_db()
#             my_db.execute(
#                 'UPDATE swStatistics SET'
#                 '   isExterior = ?,'
#                 '   minTemperature = ?,'
#                 '   maxTemperature = ?,'
#                 '   humidity = ?,'
#                 '   pressure = ?'
#                 ' WHERE id = ?',
#                 (isExterior, minTemperature, maxTemperature, humidity, pressure, id)
#             )
#             my_db.commit()
#             return redirect(url_for('statistics.index'))

#     return render_template('statistics/update.html', statistics=statistics)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @auth.login_required
# def delete(id):
#     my_db = db.get_db()
#     my_db.execute('DELETE FROM swStatistics WHERE id = ?', (id,))
#     my_db.commit()
#     return redirect(url_for('statistics.index'))


