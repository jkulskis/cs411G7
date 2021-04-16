import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session, url_for
from playlist_maker.spotify.spotify import SpotifyHandler

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
  """
