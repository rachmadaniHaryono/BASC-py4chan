"""main module."""
from logging.handlers import TimedRotatingFileHandler
from urllib.parse import unquote_plus
import logging
import os
import shutil
import tempfile

from appdirs import user_data_dir
from flask import Flask, request, flash, send_from_directory, jsonify, redirect, url_for
from flask.cli import FlaskGroup
from flask.views import View
from flask_admin import Admin, BaseView, expose
from flask_admin._compat import text_type
from flask_admin.contrib.sqla import fields, ModelView
from flask_migrate import Migrate
from sqlalchemy.orm.util import identity_key
import click

from . import views


APP_DATA_DIR = user_data_dir('basc_py4chan_server', 'rachmadaniharyono')


def get_pk_from_identity(obj):
    """Monkey patck to fix flask-admin sqla error.

    https://github.com/flask-admin/flask-admin/issues/1588
    """
    res = identity_key(instance=obj)
    cls, key = res[0], res[1]  # NOQA
    return u':'.join(text_type(x) for x in key)


fields.get_pk_from_identity = get_pk_from_identity


def create_app(script_info=None):
    """create app."""
    app = Flask(__name__)
    # logging
    if not os.path.exists(APP_DATA_DIR):
        os.makedirs(APP_DATA_DIR)
    log_dir = os.path.join(APP_DATA_DIR, 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    default_log_file = os.path.join(log_dir, 'basc_py4chan_server.log')
    file_handler = TimedRotatingFileHandler(default_log_file, 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)
    # reloader
    reloader = app.config['TEMPLATES_AUTO_RELOAD'] = \
        bool(os.getenv('BASC_PY4CHAN_SERVER_RELOADER')) or app.config['TEMPLATES_AUTO_RELOAD']  # NOQA
    if reloader:
        app.jinja_env.auto_reload = True
    # app config
    database_path = 'basc_py4chan.db'
    database_exist = os.path.isfile(database_path)
    database_uri = 'sqlite:///' + database_path
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        os.getenv('BASC_PY4CHAN_SERVER_SQLALCHEMY_DATABASE_URI') or database_uri # NOQA
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('BASC_PY4chan_SERVER_SECRET_KEY') or os.urandom(24)
    app.config['WTF_CSRF_ENABLED'] = False
    # debug
    debug = app.config['DEBUG'] = bool(os.getenv('BASC_PY4CHAN_SERVER_DEBUG')) or app.config['DEBUG']
    if debug:
        app.config['DEBUG'] = True
        app.config['LOGGER_HANDLER_POLICY'] = 'debug'
        logging.basicConfig(level=logging.DEBUG)
        # pprint.pprint(app.config)
        print('Log file: {}'.format(default_log_file))
    # app and db
    # models.db.init_app(app)
    app.app_context().push()
    # models.db.create_all()

    # default value for database
    if not database_exist:
        pass

    @app.shell_context_processor
    def shell_context():
        return {'app': app, 'db': models.db}

    # Migrate(app, models.db)
    # flask-admin
    app_admin = Admin(
        app, name='BASC PY4chan SERVER', template_mode='bootstrap3',
        index_view=views.HomeView(name='Home', template=views.INDEX_TEMPLATE, url='/'))  # NOQA

    # routing
    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """This is a script for application."""
    pass


if __name__ == "__main__":
    cli()
