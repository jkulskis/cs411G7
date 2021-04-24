import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session, url_for
from playlist_maker.utils.spotify import SpotifyHandler

mot_blueprint = Blueprint('mot_bp', __name__, template_folder='templates')

@mot_blueprint.route('/mot', methods=['GET', 'POST'])
def form():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return redirect('/')
  if request.method == "GET":
    return render_template(
      'mot.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  # POST
  if 'walking' in request.form:
    session['user_choices']['mot'] = 'walking'
  elif 'driving' in request.form:
    session['user_choices']['mot'] = 'driving'
  elif 'biking' in request.form:
    session['user_choices']['mot'] = 'bicycling'
  else: # something wrong happened. render mot page again
    return render_template(
      'mot.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  return redirect(url_for("speed_bp.form")) 
