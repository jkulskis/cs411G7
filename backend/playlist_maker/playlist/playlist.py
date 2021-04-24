from flask import Blueprint, request, redirect, render_template, current_app, session, url_for
from playlist_maker.utils.spotify import SpotifyHandler
from playlist_maker.utils.location import Location

playlist_blueprint = Blueprint('playlist_bp', __name__, template_folder='templates')

@playlist_blueprint.route('/playlist', methods=['GET','POST'])
def get_playlist():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return redirect('/')
  if request.method == "GET":
    return render_template(
      'playlist.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  # POST
  # At this point, we should have all of the user data that we
  # need to form the playlist

  # Start off by initializing the locations
  origin = Location(address=session['user_choices']['origin'])
  # init_geo is False for destination since we really just need the address...avoid an extra API call
  destination = Location(address=session['user_choices']['destination'], init_geo=False)
  # find the duration between and store in the session
  session['duration'] = origin.duration_between(
    destination, 
    mot=session['user_choices']['mot']
  )
  # change duration according to user speed (for normal just leave the same)
  if session['user_choices']['speed'] == 'faster':
    session['duration'] *= 1.2 # 20% speed increase
  elif session['user_choices']['speed'] == 'slower':
    session['duration'] *= 0.2 # 20% speed decrease
  # get the weather status at the origin for our weather data
  session['weather_status'] = origin.weather_now()
  # create the playlist using the spotify handler with the weather and duration constraints
  final_playlist, total_time = spotify.create_playlist(
    weather_status=session['weather_status'], 
    duration=session['duration']
  )
  # for now just display the data...the playlist should be added to the account now too
  return f"""
  <h1>Data Crunching Time :P</h1>
  <i>Origin</i>: {session['user_choices']['origin']}
  <br>
  <i>Destination</i>: {session['user_choices']['destination']}
  <br>
  <i>Mode of transport</i>: {session['user_choices']['mot']}
  <br>
  <i>Actual duration</i>: {session['duration']}
  <br>
  <i>Speed</i>: {session['user_choices']['speed']}
  <br>
  <i>Temperature</i>: {origin.temperature}
  <br>
  <i>Weather</i>: {origin.weather_status}
  <br>
  <i>Total time</i>: {total_time}
  <br>
  <i>Playlist<i/>: <br>{
    '<br>'.join(
      [
        track['track']['name'] + ': ' + track['track']['id'] for track in final_playlist['tracks']['items']
      ]
    )
  }
  """
