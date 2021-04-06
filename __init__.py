from flask import Flask

from app.auth.auth import auth_blueprint
from app.home.home import home_blueprint
from app.maps.mapping import map_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py') # need to make your own config file
    app.config['SECRET_KEY'] = 'JUSTARANDOMKEY' # ngl have no idea what exactly this this for

    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(map_blueprint)
    return app