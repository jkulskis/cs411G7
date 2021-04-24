from flask import render_template, request, redirect, session, url_for, Blueprint
from playlist_maker.utils.spotify import SpotifyHandler

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
    # go straight to travel, already signed in
    return redirect(url_for("travel_bp.form")) 

@home_blueprint.route("/callback/spotify")
def callback():
    """
    set the session's authorization header
    """
    spotify = SpotifyHandler()
    if request.args.get("code"): # code in args, grab it and add to auth
        # Being redirected from Spotify auth page. Grab token and redirect to travel
        spotify.auth_manager.get_access_token(request.args.get("code"))
        session['display_name'] = spotify.me()['display_name']
    if spotify.valid_token():
        return redirect(url_for("travel_bp.form"))
    return redirect('/') # Something went wrong. Redirect back to home