from flask import Blueprint, request, redirect, render_template, current_app, session
from playlist_maker.cache import get_cache_handler
import googlemaps
import spotipy
from spotipy import SpotifyOAuth
# from app import app as app <-- won't work

map_blueprint = Blueprint('map_bp', __name__, template_folder='templates')

# won't work
# with app.app_context():
#     google_api_key = current_app.config['GOOGLE_API_KEY']
#     gmaps = googlemaps.Client(key=google_api_key)

@map_blueprint.route('/form')
def form():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            cache_handler=get_cache_handler(),
            scope=current_app.config['SPOTIFY_SCOPE'],
            client_id=current_app.config['SPOTIFY_CLIENT_ID'],
            client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
            redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI']
        ), 
    )
    if not sp.auth_manager.validate_token(get_cache_handler().get_cached_token()):
        return redirect('/')
    return render_template('form.html', name=sp.me()['display_name'])

@map_blueprint.route('/request', methods=['GET','POST'])
def get_distance():
    google_api_key = current_app.config['GOOGLE_API_KEY']
    gmaps = googlemaps.Client(key=google_api_key)

    origin = request.form['origin']
    destination = request.form['destination']
    mode = request.form['mode']


    data = gmaps.distance_matrix(origin, destination, mode=mode, region='US')
    duration = data["rows"][0]["elements"][0]["duration"]["value"]

    return render_template('display_distance.html', data=data, duration=duration)


