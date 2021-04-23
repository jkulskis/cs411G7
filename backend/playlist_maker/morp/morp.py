from flask import Blueprint, request, redirect, render_template, current_app, session, url_for
from playlist_maker.utils.spotify import SpotifyHandler

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
  else: # something wrong happened. Render morp page again
    return render_template(
      'morp.html', 
      name=session['display_name'],
      user_choices=session['user_choices']
    )
  return redirect(url_for("playlist_bp.get_playlist")) 
