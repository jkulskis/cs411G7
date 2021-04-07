import spotipy
from flask import Blueprint, request, redirect, url_for, session, current_app
from spotipy.oauth2 import SpotifyOAuth
from playlist_maker.cache import get_cache_handler
# from app import app <-- this won't work

auth_blueprint = Blueprint('auth_bp', __name__)

@auth_blueprint.route("/login", methods=['POST', 'GET'])
def login():
    """
    redirect to Spotify's log in page
    """
    auth_manager = SpotifyOAuth(
        cache_handler=get_cache_handler(),
        scope=current_app.config['SPOTIFY_SCOPE'],
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI']
    )
    if not auth_manager.validate_token(get_cache_handler().get_cached_token()):
        # no token, redirect to auth URL to get the token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    else:
        return redirect(url_for("map_bp.form")) # go straight to map, already signed in


@auth_blueprint.route("/callback/spotify")
def callback():
    """
    set the session's authorization header
    """
    auth_manager = SpotifyOAuth(
        cache_handler=get_cache_handler(),
        scope=current_app.config['SPOTIFY_SCOPE'],
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI']
    )
    if request.args.get("code"):
        print("here")
        # Being redirected from Spotify auth page. Grab token and redirect back to login
        auth_manager.get_access_token(request.args.get("code"))
        return redirect(url_for("map_bp.form"))
    return redirect(url_for("map_bp.form")) # we've signed in, now go to the map