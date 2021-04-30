import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session, url_for, jsonify
from playlist_maker.utils.spotify import SpotifyHandler

speed_blueprint = Blueprint('speed_bp', __name__, template_folder='templates')

@speed_blueprint.route('/speed', methods=['GET', 'POST'])
def form():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return jsonify("Access Denied"), 401
  if request.method == "GET":
    return jsonify(dict(session)), 200
  # POST
  speed = request.json.get('speed')
  if speed == 'slower':
    session['user_choices']['speed'] = 'slower'
  elif speed == 'normal':
    session['user_choices']['speed'] = 'normal'
  elif speed == 'faster':
    session['user_choices']['speed'] = 'faster'
  else: # invalid request args
    return jsonify({
      'display_name': session['display_name'],
      'user_choices': session['user_choices']
    }), 400
  return jsonify({
    'display_name': session['display_name'],
    'user_choices': session['user_choices']
  }), 200
