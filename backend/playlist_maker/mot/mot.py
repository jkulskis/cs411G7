import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session, url_for, jsonify
from playlist_maker.utils.spotify import SpotifyHandler

mot_blueprint = Blueprint('mot_bp', __name__, template_folder='templates')

@mot_blueprint.route('/mot', methods=['GET', 'POST'])
def form():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return jsonify("Access Denied"), 401
  if request.method == "GET":
    return jsonify({
      'display_name': session['display_name'],
      'user_choices': session['user_choices']
    }), 200
  # POST
  mot = request.json.get('mot')
  if mot == 'walking':
    session['user_choices']['mot'] = 'walking'
  elif mot == 'driving':
    session['user_choices']['mot'] = 'driving'
  elif mot == 'biking':
    session['user_choices']['mot'] = 'bicycling'
  else: # Invalid request args
    return jsonify({
      'display_name': session['display_name'],
      'user_choices': session['user_choices']
    }), 400
  return jsonify({
    'display_name': session['display_name'],
    'user_choices': session['user_choices']
  }), 200
