import os
import uuid

from spotipy import SpotifyOAuth, Spotify, CacheHandler, CacheFileHandler
from flask import session, current_app

# NOTE: Could also do RedisCacheHandler if we want to use Redis instead
class MongoCacheHandler(CacheHandler):
  def __init__(self):
    raise NotImplementedError

"""
One of the reasons that we create a spotify handler to wrap the spotipy Spotify class
is so that we can condense code every time we need to create an auth manager, add the cache,
and check if the token is valid. We turn the following code:

  auth_manager = SpotifyOAuth(
      cache_handler=self.get_cache_handler(),
      scope=current_app.config['SPOTIFY_SCOPE'],
      client_id=current_app.config['SPOTIFY_CLIENT_ID'],
      client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
      redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI']
  )
  if not auth_manager.validate_token(cache_handler.get_cached_token()):
      return redirect('/')
  spotify = spotipy.Spotify(auth_manager=auth_manager)

into:

  spotify = SpotifyHandler()
  if not spotify.valid():
    return redirect('/')

This helps a lot since we need to grab from the spotify cache and initiate an object
when we get a new request in the flask app.
"""
class SpotifyHandler(Spotify):

  # TODO: Get a mongo cache handler isntead of a file cache handler
  def get_cache_handler(self):
    """Gets a cache handler to cache the spotify oauth token info in
    """
    if not os.path.exists(current_app.config['SPOTIFY_CACHES_DIR']):
      os.makedirs(current_app.config['SPOTIFY_CACHES_DIR'])
    if not session.get('uuid'):
      session['uuid'] = str(uuid.uuid4()) # Unknown user for the handler, give random ID
    cache_path = f"{current_app.config['SPOTIFY_CACHES_DIR']}/{session.get('uuid')}"
    return CacheFileHandler(cache_path=cache_path)

  def __init__(self):
    super().__init__()
    self.auth_manager = SpotifyOAuth(
        cache_handler=self.get_cache_handler(),
        scope=current_app.config['SPOTIFY_SCOPE'],
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI']
    )
  
  def valid_token(self):
    """Returns true if the oauth token is valid, false otherwise
    """
    if not self.auth_manager.validate_token(self.get_cache_handler().get_cached_token()):
      return False
    return True

