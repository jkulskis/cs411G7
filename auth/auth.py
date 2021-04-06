from flask import Blueprint, request, redirect, url_for, session, current_app

from app.spotify_api.spotify_client import SpotifyClient
# from app import app <-- this won't work

auth_blueprint = Blueprint('auth_bp', __name__)


# won't work
# with app.app_context():
#     client_id = current_app.config['SPOTIFY_CLIENT_ID']
#     client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
#     spotify_client = SpotifyClient(client_id, client_secret, port=5000)


@auth_blueprint.route("/login", methods=['POST', 'GET'])
def login():
    """
    redirect to Spotify's log in page
    """
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
    spotify_client = SpotifyClient(client_id, client_secret, port=5000)

    auth_url = spotify_client.get_auth_url()
    return redirect(auth_url)


@auth_blueprint.route("/callback/q")
def callback():
    """
    set the session's authorization header
    """
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
    spotify_client = SpotifyClient(client_id, client_secret, port=5000)

    auth_token = request.args['code']
    spotify_client.get_authorization(auth_token)
    authorization_header = spotify_client.authorization_header
    session['authorization_header'] = authorization_header
    return redirect(url_for("map_bp.form"))