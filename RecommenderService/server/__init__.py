from flask import Flask
import os


def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_instance_folder_path():
    return os.path.join(get_app_base_path(), 'instance')


config = {
    "dev": "config.DevelopmentConfig",
    "prod": "config.ProductionConfig",
    "default": "config.DevelopmentConfig"
}

config_name = os.getenv('FLASK_ENV', "dev")
app = Flask(__name__)
app.config.from_object(config[config_name])
app.config.from_pyfile('config.py', silent=True)
