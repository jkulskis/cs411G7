import os
from flask import Flask
from flask_session import Session

from playlist_maker.home.home import home_blueprint
from playlist_maker.travel.travel import travel_blueprint
from playlist_maker.mot.mot import mot_blueprint
# from playlist_maker.morp.morp import morp_blueprint
from playlist_maker.speed.speed import speed_blueprint
from playlist_maker.playlist.playlist import playlist_blueprint

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py') # need to make your own config file

    app.config['SECRET_KEY'] = os.urandom(64)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    Session(app) # server-side session to the app. access the Session instance with the session imported from flask

    app.register_blueprint(home_blueprint) # home to help login if not already logged in
    app.register_blueprint(travel_blueprint) # travel...choose start and end destinations
    app.register_blueprint(mot_blueprint) # mode of transport (walking, driving, biking)
    app.register_blueprint(speed_blueprint) # speed = how fast (slower/normal/faster)
    # app.register_blueprint(morp_blueprint) # morp = music or podcast
    app.register_blueprint(playlist_blueprint) # create / show playlist
    return app
