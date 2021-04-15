import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session
from playlist_maker.spotify.spotify import SpotifyHandler

mot_blueprint = Blueprint('mot_bp', __name__, template_folder='templates')

@mot_blueprint.route('/mot', methods=['GET', 'POST'])
def form():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return redirect('/')
  if request.method == "GET":
    return render_template(
      'mot.html', 
      name=spotify.me()['display_name']
    )
  # POST
  if 'walking' in request.form:
    session['mot'] = 'walking'
  elif 'driving' in request.form:
    session['mot'] = 'driving'
  elif 'biking' in request.form:
    session['mot'] = 'biking'
  else: # something wrong happened. render mot page again
    return render_template(
      'mot.html', 
      name=spotify.me()['display_name']
    )
  return f"""
  <h1>Speed page</h1>
  Origin: {session['origin']}
  <br>
  Destination: {session['destination']}
  <br>
  Mode of transport: {session['mot']}
  """
