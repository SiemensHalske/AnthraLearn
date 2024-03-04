import os
from flask import Flask
from flask_jwt_extended import JWTManager
from .main.routes import main_bp
from .auth.routes import auth_bp
from .models import db


def create_app():
    app = Flask('AnthraLearn')
    app.template_folder = 'app\\templates'
    app.static_folder = 'app\\static'

    print(f'Template path: {app.template_folder}')
    print(f'Static path: {app.static_folder}')

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    app.config['MAX_CONCURRENT_CONNECTION'] = 4
    # app.config['SERVER_NAME'] = 'AnthraLearn'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.secret_key = os.urandom(24).hex()
    app.config['SESSION_COOKIE_NAME'] = 'AnthraLearn_session'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    jwt_secret_key = None
    with open('app\\jwt_key.cert', 'r', encoding='utf-8') as certificate:
        jwt_secret_key = certificate.read()

    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_SECRET_KEY'] = jwt_secret_key
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # CSRF protection

    user = 'postgres'
    password = 'zoRRo123?'
    host = 'localhost'
    port = '5432'
    name = 'AnthraLearn'

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt = JWTManager(app)  # Initialize the JWTManager extension

    return app
