import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session, url_for
from playlist_maker.spotify.spotify import SpotifyHandler
from pyowm.owm import OWM

morp_blueprint = Blueprint('morp_bp', __name__, template_folder='templates')

@morp_blueprint.route('/morp', methods=['GET', 'POST'])
def form():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return redirect('/')
  if request.method == "GET":
    return render_template(
      'morp.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  
  # weather api
  owm = OWM('46aea01cbd4afd5057ea0fbb49d6e0a3')
  mgr = owm.weather_manager()

  # get current location from cache
  google_api_key = current_app.config['GOOGLE_API_KEY']
  gmaps = googlemaps.Client(key=google_api_key)
  # grab the form values
  origin = session['user_choices']['origin']
  origin_coded = gmaps.geocode(origin)
  origin_lat = origin_coded[0]["geometry"]["location"]["lat"]
  origin_long = origin_coded[0]["geometry"]["location"]["lng"]

  weather = mgr.weather_at_coords(origin_lat, origin_long).weather
  temp = weather.temperature('fahrenheit')["temp"]
  weather_details = weather.detailed_status

  # POST
  if 'music' in request.form:
    session['user_choices']['morp'] = 'music'
  elif 'podcast' in request.form:
    session['user_choices']['morp'] = 'podcast'
  else: # something wrong happened. render mot page again
    return render_template(
      'morp.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  # for now just display the data
  return f"""
  <h1>Data Crunching Time :P</h1>
  <i>Origin</i>: {session['user_choices']['origin']}
  <br>
  <i>Destination</i>: {session['user_choices']['destination']}
  <br>
  <i>Mode of transport</i>: {session['user_choices']['mot']}
  <br>
  <i>Speed</i>: {session['user_choices']['speed']}
  <br>
  <i>Music or Podcast</i>: {session['user_choices']['morp']}
  <br>
  <i>Temperature</i>: {temp}
  <br>
  <i>Weather</i>: {weather_details}
  """
