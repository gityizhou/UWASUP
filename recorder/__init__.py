from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from recorder.config import app_config
from flask_uploads import UploadSet, configure_uploads, ALL
from flask_mail import Mail

db = SQLAlchemy()  # db initialization
migrate = Migrate()
# manage user session
loginManager = LoginManager()

loginManager.login_view = 'index'
mail = Mail()


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
    mail.init_app(app)

    # app route url
    from recorder.route import index, not_activated, student_view, teacher_view, logout, register, upload, reset_password_request, \
        password_reset, request_email_verification, verify_email_by_token, task_result_downloader, teacher_recorder, \
        pdf_upload, page_404, page_500
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/not_activated', 'not_activated', not_activated)
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    app.add_url_rule('/student/<student_number>', 'student_view', student_view, methods=['GET', 'POST'])
    app.add_url_rule('/teacher/<staff_number>', 'teacher_view', teacher_view, methods=['GET', 'POST'])
    app.add_url_rule('/recorder', 'recorder', upload, methods=['GET', 'POST'])
    app.add_url_rule('/teacher_recorder', 'teacher_recorder', teacher_recorder, methods=['GET', 'POST'])
    app.add_url_rule('/pdf_upload', 'pdf_upload', pdf_upload, methods=['GET', 'POST'])
    app.add_url_rule('/download_csv/sakjhuzhcu213huhd8sacukkd/<task_id>', 'download_csv', task_result_downloader,
                     methods=['GET', 'POST'])

    # #download
    # app.add_url_rule('/listfiles', 'listfiles',getFilesList)
    # app.add_url_rule('/downloads/<filename>', 'send_download',download_access)
    # app.add_url_rule('/download/<id>/<title>', 'download',donwload)

    # verify email
    app.add_url_rule('/request_email_verify', 'request_email_verify', request_email_verification)
    app.add_url_rule('/verify_email_by_token/<token>', 'verify_email_by_token', verify_email_by_token)

    app.add_url_rule(
        '/reset_password_request',
        'reset_password_request',
        reset_password_request,
        methods=['GET', 'POST']
    )
    app.add_url_rule(
        '/password_reset/<token>',
        'password_reset',
        password_reset,
        methods=['GET', 'POST']
    )

    app.register_error_handler(404, page_404)
    app.register_error_handler(500, page_500)

    return app
