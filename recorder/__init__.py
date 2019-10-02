from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from recorder.config import app_config
from flask_uploads import UploadSet, configure_uploads, ALL

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
    files = UploadSet('files', ALL)
    # app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
    configure_uploads(app, files)

    # app route url
    from recorder.route import index, student_view, teacher_view, logout, register, upload
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    app.add_url_rule('/student/<student_number>', 'student_view', student_view, methods=['GET', 'POST'])
    app.add_url_rule('/teacher/<staff_number>', 'teacher_view', teacher_view, methods=['GET', 'POST'])
    app.add_url_rule('/recorder', 'recorder', upload, methods=['GET', 'POST'])

    return app
