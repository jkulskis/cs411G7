import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session
from playlist_maker.spotify.spotify import SpotifyHandler

map_blueprint = Blueprint('map_bp', __name__, template_folder='templates')

@map_blueprint.route('/mapping', methods=['GET'])
def form():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return redirect('/')
  if request.method == "GET":
    return render_template(
      'mapping.html', 
      name=spotify.me()['display_name']
    )
  elif request.method == "POST":
    return get_distance()

@map_blueprint.route('/mapping', methods=['POST'])
def display_distance():
  # set up gmaps client
  google_api_key = current_app.config['GOOGLE_API_KEY']
  gmaps = googlemaps.Client(key=google_api_key)
  # grab the form values
  origin = request.form['origin']
  destination = request.form['destination']
  mode = request.form['mode']
  # get the response from gmaps
  data = gmaps.distance_matrix(origin, destination, mode=mode, region='US')
  duration = data["rows"][0]["elements"][0]["duration"]["value"]

  return render_template('display_distance.html', data=data, duration=duration)


