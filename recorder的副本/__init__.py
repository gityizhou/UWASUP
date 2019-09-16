from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from recorder.config import app_config

db = SQLAlchemy()  # db initialization
migrate = Migrate()
# manage user session
loginManager = LoginManager()

loginManager.login_view = 'index'

# config_name: you can change to test environment by changing development to 'testing'
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)  # db initialization
    migrate.init_app(app, db)  # db migrate initialization
    loginManager.init_app(app)

    # app route url
    from recorder.route import index, student_view, teacher_view, logout, register, upload, download, show_result
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    app.add_url_rule('/student/<username>', 'student_view', student_view, methods=['GET', 'POST'])
    app.add_url_rule('/teacher_view', 'teacher_view', teacher_view, methods=['GET', 'POST'])
    app.add_url_rule('/upload', 'upload', upload, methods=['GET', 'POST'])
    app.add_url_rule('/download', 'download', download, methods=['GET', 'POST'])
    # result for uploading a mp3
    app.add_url_rule('/result', 'result', show_result)

    return app
