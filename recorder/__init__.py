from flask import Flask
from recorder.route import hello


def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', 'index', hello)
    app.add_url_rule('/index', 'index', hello)

    return app
