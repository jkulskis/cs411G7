import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session, url_for, jsonify
from playlist_maker.utils.spotify import SpotifyHandler

travel_blueprint = Blueprint('travel_bp', __name__, template_folder='templates')

@travel_blueprint.route('/travel', methods=['GET', 'POST'])
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
  origin = request.args.get('origin')
  destination = request.args.get('destination')
  if origin and destination:
    session['user_choices']['origin'] = origin
    session['user_choices']['destination'] = destination
    return jsonify({
      'display_name': session['display_name'],
      'user_choices': session['user_choices']
    }), 200
  # need origin & destination args
  return jsonify({
    'display_name': session['display_name'],
    'user_choices': session['user_choices']
  }), 400
