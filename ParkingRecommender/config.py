import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
    ENV = "dev"
    PORT = 1500
    PARKING_METERS_SERVICE = {
        'HOST': "http://localhost",
        'PORT': '2500',
        'PATH': "parking_meters/all"
    }
    HAVERSINE_DISTANCE_SERVICE = {
        'HOST': "http://localhost",
        'PORT': '3500',
        'PATH': "distance/get_distance"
    }
    PARKING_RECOMMENDER_SERVICE = {
        'HOST': "http://localhost",
        'PORT': '4500',
        'PATH': "predict"
    }


class ProductionConfig(BaseConfig):
    DEVELOPMENT = False
    DEBUG = False
    ENV = "prod"
    PORT = 1500
    PARKING_METERS_SERVICE = {
        'HOST': "http://parkingmeters-service",
        'PORT': '2500',
        'PATH': "parking_meters/all"
    }
    HAVERSINE_DISTANCE_SERVICE = {
        'HOST': "http://coordinate-distance-service",
        'PORT': '3500',
        'PATH': "distance/get_distance"
    }
    PARKING_RECOMMENDER_SERVICE = {
        'HOST': "http://parking-recommender-service",
        'PORT': '4500',
        'PATH': "predict"
    }


config = {
    "dev": "config.DevelopmentConfig",
    "prod": "config.ProductionConfig",
    "default": "config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONF', "default")
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py', silent=True)
