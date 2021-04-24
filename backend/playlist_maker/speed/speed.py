import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session, url_for
from playlist_maker.utils.spotify import SpotifyHandler

speed_blueprint = Blueprint('speed_bp', __name__, template_folder='templates')

@speed_blueprint.route('/speed', methods=['GET', 'POST'])
def form():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return redirect('/')
  if request.method == "GET":
    return render_template(
      'speed.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  # POST
  if 'slower' in request.form:
    session['user_choices']['speed'] = 'slower'
  elif 'normal' in request.form:
    session['user_choices']['speed'] = 'normal'
  elif 'faster' in request.form:
    session['user_choices']['speed'] = 'faster'
  else: # something wrong happened. render mot page again
    return render_template(
      'speed.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  return redirect(url_for("playlist_bp.get_playlist")) 
