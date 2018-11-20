import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
    ENV = "dev"
    PORT = 1500



class ProductionConfig(BaseConfig):
    DEVELOPMENT = False
    DEBUG = False
    ENV = "prod"
    PORT = 1500


config = {
    "dev": "config.DevelopmentConfig",
    "prod": "config.ProductionConfig",
    "default": "config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONF', "default")
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py', silent=True)
