import os

config_path = os.path.abspath(os.path.dirname(__file__))

"""
two environments for development and testing, can change environment in __init__.py
using different database

"""
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_DEFAULT_DEST = 'uploads'


class TestingConfig(Config):
    SECRET_KEY = "CITS-5206"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(config_path, 'unittest.db')
                                             + '?check_same_thread=False')


class DevelopmentConfig(Config):
    SECRET_KEY = "zxc47POI"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(config_path, 'record.db')
                                             + '?check_same_thread=False')


app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig
}