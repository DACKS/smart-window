import os
from . import db
from . import auth
from . import userRole
from . import interval
from . import notification
from . import notificationType
from . import statistics

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(interval.bp)
    app.register_blueprint(userRole.bp)
    app.register_blueprint(notification.bp)
    app.register_blueprint(notificationType.bp)
    app.register_blueprint(statistics.bp)

    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    return app
    