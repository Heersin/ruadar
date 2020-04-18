from flask import Flask,url_for
from flask_login import LoginManager
from flask_dropzone import Dropzone
from conf.config import config
import logging
from logging.config import fileConfig
import os

fileConfig('conf/log-app.conf')

dropzone = Dropzone()


def get_logger(name):
    return logging.getLogger(name)


def get_basedir():
    return os.path.abspath(os.path.dirname(__file__))


def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # dropzone here
    dropzone.init_app(app)


    from .admin import admin as main_blueprint
    app.register_blueprint(main_blueprint)


    return app
