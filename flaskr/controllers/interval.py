import functools
from os import name
import json
from datetime import date, datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)

from flaskr.storage import db
from flaskr.controllers import auth


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

bp = Blueprint('intervals', __name__, url_prefix='/intervals')
bp_api = Blueprint('api-intervals', __name__, url_prefix='/api/intervals')

@bp.route('/', methods=['GET'])
def index():
    my_db = db.get_db()
    intervals = my_db.execute(
        'SELECT *'
        ' FROM interval'
        ' ORDER BY createdAt DESC'
    ).fetchall()
    return render_template('intervals/index.html', intervals=intervals)

@bp_api.route('/', methods=['GET', 'POST'])
def api_index():
    try:
        my_db = db.get_db()
        intervals = my_db.execute(
            'SELECT *'
            ' FROM interval'
            ' ORDER BY createdAt DESC'
        ).fetchall()
        return json.dumps( [dict(interval) for interval in intervals], default=str)
    except:
        return jsonify({'error': 'An error occured related to database...'})


@bp.route('/create', methods=('GET', 'POST'))
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
            return redirect(url_for('intervals.index'))

    return render_template('intervals/create.html')


@bp_api.route('/create', methods=( 'POST',))
@auth.login_required
def api_create():
    try:
        name = request.json['name']
    except:
        return jsonify({'error': 'name is missing...'})
    try:
        iStart = request.json['iStart']
    except:
        return jsonify({'error': 'iStart is missing...'})
    try:
        iEnd = request.json['iEnd']
    except:
        return jsonify({'error': 'iEnd is missing...'})
    try:
        luminosity = request.json['luminosity']
    except:
        return jsonify({'error': 'luminosity is missing...'})

    try: 
        iStart = datetime.strptime(iStart, DATE_FORMAT)
    except:
        return jsonify({'error': 'iStart is not formatted properly...'})

    try: 
        iEnd = datetime.strptime(iEnd, DATE_FORMAT)
    except:
        return jsonify({'error': 'iEnd is not formatted properly...'})

    try:
        my_db = db.get_db()
        my_db.execute(
            'INSERT INTO interval (name, iStart, iEnd, luminosity)'
            ' VALUES (?, ?, ?, ?)',
            (name, iStart, iEnd, luminosity)
        )
        my_db.commit()
        return jsonify({'message': 'Interval has been created with success!'})
    except:
        return jsonify({'error': 'An error occured related to database...'})


def get_interval(id, from_api=False):
    interval = db.get_db().execute(
        'SELECT *'
        ' FROM interval'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if interval is None:
        if from_api:
            return None
        abort(404, f"Interval id {id} doesn't exist.")

    # if check_user and interval['userID'] != g.user['id']:
    #     abort(403)

    return interval


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
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
            return redirect(url_for('intervals.index'))


@bp_api.route('/<int:id>/update', methods=('POST',))
@auth.login_required
def api_update(id):
    interval = get_interval(id, from_api=True)

    if request.method == 'POST':
          
        try:
            name = request.json['name']
        except:
            return jsonify({'error': 'name is missing...'})
        try:
            iStart = request.json['iStart']
        except:
            return jsonify({'error': 'iStart is missing...'})
        try:
            iEnd = request.json['iEnd']
        except:
            return jsonify({'error': 'iEnd is missing...'})
        try:
            luminosity = request.json['luminosity']
        except:
            return jsonify({'error': 'luminosity is missing...'})

        try: 
            iStart = datetime.strptime(iStart, DATE_FORMAT)
        except:
            return jsonify({'error': 'iStart is not formatted properly...'})

        try: 
            iEnd = datetime.strptime(iEnd, DATE_FORMAT)
        except:
            return jsonify({'error': 'iEnd is not formatted properly...'})

        
        try: 
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
            return jsonify({'message': f'Interval {id} was updated with success!'})
        except:
            return jsonify({'error': 'An error occured related to database...'})



@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    my_db = db.get_db()
    my_db.execute('DELETE FROM interval WHERE id = ?', (id,))
    my_db.commit()
    return redirect(url_for('intervals.index'))

@bp_api.route('/<int:id>/delete', methods=('GET',))
@auth.login_required
def api_delete(id):
    interval = get_interval(id, from_api=True)
    if interval is None:
        return jsonify({'error': f'There is no interval with id {id}'})
    try:
        my_db = db.get_db()
        my_db.execute('DELETE FROM interval WHERE id = ?', (id,))
        my_db.commit()
        return jsonify({'message': f'Inteval {id} has been deleted with success!'})
    except:
        return jsonify({'error': 'An error occured related to database...'})