import os
from flask import Flask
from .main.routes import main_bp
from .auth.routes import auth_bp


def create_app():
    app = Flask('AnthraLearn')
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    app.config['MAX_CONCURRENT_CONNECTION'] = 4
    # app.config['SERVER_NAME'] = 'AnthraLearn'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.secret_key = os.urandom(24).hex()
    app.config['SESSION_COOKIE_NAME'] = 'AnthraLearn_session'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    return app
