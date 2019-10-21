import os

config_path = os.path.abspath(os.path.dirname(__file__))

"""
two environments for development and testing, can change environment in __init__.py
using different database
"""
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_DEFAULT_DEST = 'uploads'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@recorder.com')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 1)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'languageapp19@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'L@nguageapp19')
    MAIL_SUBJECT_RESET_PASSWORD = '[Recorder] Please Reset Your Password'
    MAIN_SUBJECT_USER_ACTIVATE = '[Recorder] Please Activate Your Accout'



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
