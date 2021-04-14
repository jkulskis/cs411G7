import os
from flask import Flask
from flask_session import Session

from playlist_maker.home.home import home_blueprint
from playlist_maker.maps.mapping import map_blueprint

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py') # need to make your own config file

    app.config['SECRET_KEY'] = os.urandom(64)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    Session(app) # server-side session to the app. access the Session instance with the session imported from flask

    app.register_blueprint(home_blueprint)
    # app.register_blueprint(auth_blueprint)
    app.register_blueprint(map_blueprint)
    return app
