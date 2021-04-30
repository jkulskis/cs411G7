from flask import render_template, request, redirect, session, url_for, Blueprint, jsonify
from playlist_maker.utils.spotify import SpotifyHandler
import time

home_blueprint = Blueprint('home_bp', __name__, template_folder='templates')

def check_manual_token(spotify_handler):
    """If you are sending a request manually using something like postman, and include a bearer token
    for spotify, this will check for it and save it to the cache. This assumes that the token is not
    expired. Normally, the user would authenticate using a redirect url from the backend, so this
    is for development purposes
    """
    if request.headers.get('Authorization'):
        access_token = request.headers.get('Authorization').split()[1]
        spotify_handler.get_cache_handler().save_token_to_cache(
          {
            'access_token': access_token,
            'expires_in': 3600,
            'scope': 'user-library-read playlist-modify-public playlist-read-collaborative',
            'expires_at': int(time.time()) + 3600,
          }
        )

@home_blueprint.route("/login")
def home():
    spotify = SpotifyHandler()
    check_manual_token(spotify_handler=spotify)
    if not spotify.valid_token(): # no code or code invalid, provide home template asking them to login
        auth_url = spotify.auth_manager.get_authorize_url()
        # return redirect(auth_url)
        return jsonify({
          'auth_url': auth_url
        }), 401
    if request.args.get("code"): # code in args, grab it and add to auth
        spotify.auth_manager.get_access_token(request.args.get("code"))
    session['display_name'] = spotify.me()['display_name']
    # go straight to travel, already signed in
    return jsonify({
      'display_name': session['display_name'],
      'user_choices': session['user_choices']
    }), 200

@home_blueprint.route("/callback/spotify")
def callback():
    """
    set the session's authorization header
    """
    spotify = SpotifyHandler()
    check_manual_token(spotify_handler=spotify)
    if request.args.get("code"): # code in args, grab it and add to auth
        # Being redirected from Spotify auth page. Grab token and redirect to travel
        spotify.auth_manager.get_access_token(request.args.get("code"))
        session['display_name'] = spotify.me()['display_name']
    if spotify.valid_token():
        return "<script>window.onload = window.close();</script>" # close login page after successful validation
    return jsonify('Unable to handle login callback'), 500