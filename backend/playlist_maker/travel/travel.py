import googlemaps
from flask import Blueprint, request, redirect, render_template, current_app, session, url_for
from playlist_maker.utils.spotify import SpotifyHandler

travel_blueprint = Blueprint('travel_bp', __name__, template_folder='templates')

@travel_blueprint.route('/travel', methods=['GET', 'POST'])
def form():
  spotify = SpotifyHandler()
  if not spotify.valid_token():
    return redirect('/')
  if request.method == "GET":
    return render_template(
      'travel.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  # POST
  session['user_choices']['origin'] = request.form['origin']
  session['user_choices']['destination'] = request.form['destination']
  return redirect(url_for("mot_bp.form")) 
