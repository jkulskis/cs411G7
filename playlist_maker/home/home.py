from flask import render_template, request, redirect, session, url_for, Blueprint
from playlist_maker.spotify.spotify import SpotifyHandler

home_blueprint = Blueprint('home_bp', __name__, template_folder='templates')

@home_blueprint.route("/")
def home():
    spotify = SpotifyHandler()
    if not spotify.valid_token(): # no code or code invalid, provide home template asking them to login
        auth_url = spotify.auth_manager.get_authorize_url()
        return render_template('home.html', auth_url=auth_url)
    if request.args.get("code"): # code in args, grab it and add to auth
        spotify.auth_manager.get_access_token(request.args.get("code"))
    session['display_name'] = spotify.me()['display_name']
    session['user_id'] = spotify.me()['id']
    # go straight to map, already signed in
    return redirect(url_for("map_bp.form")) 

@home_blueprint.route("/callback/spotify")
def callback():
    """
    set the session's authorization header
    """
    spotify = SpotifyHandler()
    if request.args.get("code"): # code in args, grab it and add to auth
        # Being redirected from Spotify auth page. Grab token and redirect to map
        spotify.auth_manager.get_access_token(request.args.get("code"))
        session['display_name'] = spotify.me()['display_name']
        return redirect(url_for("map_bp.form"))
    return redirect('/') # no code, something went wrong. Redirect back to home