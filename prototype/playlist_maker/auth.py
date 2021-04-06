from flask import Blueprint, redirect

from app.spotify_api.spotify_client import SpotifyClient


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    '''
    redirects to Spotify's own login page
    '''
    auth_url = spotify_client.get_auth_url()
    return redirect(auth_url)