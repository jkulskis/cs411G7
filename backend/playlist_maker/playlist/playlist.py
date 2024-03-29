from flask import Blueprint, request, redirect, render_template, current_app, session, url_for, jsonify
from playlist_maker.utils.spotify import SpotifyHandler
from playlist_maker.utils.location import Location

playlist_blueprint = Blueprint('playlist_bp', __name__, template_folder='templates')

@playlist_blueprint.route('/playlist', methods=['GET'])
def get_playlist():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return jsonify("Access Denied"), 401
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
  if session['user_choices']['speed'] == 'slower':
    session['duration'] *= 1.2 # increases duration of playlist to match longer commute
  elif session['user_choices']['speed'] == 'faster':
    session['duration'] *= 0.8 # decreases duration of playlist to match shorter commute
  if session['duration'] > 48*60*60: # must be less than 48 hours
    return jsonify({
      'display_name': session['display_name'],
      'user_choices': session['user_choices'],
    }), 400
  print(session['duration'])
  if session['duration'] < 30: # no 30 second trips
    return jsonify({
      'display_name': session['display_name'],
      'user_choices': session['user_choices'],
    }), 501

  # get the weather status at the origin for our weather data
  session['weather_status'] = origin.weather_now()
  # create the playlist using the spotify handler with the weather and duration constraints
  final_playlist, total_time = spotify.create_playlist(
    weather_status=session['weather_status'], 
    duration=session['duration']
  )
  session['playlist'] = final_playlist
  # Return session with playlist
  return jsonify({
    'display_name': session['display_name'],
    'user_choices': session['user_choices'],
    'playlist': session['playlist']
  }), 200
