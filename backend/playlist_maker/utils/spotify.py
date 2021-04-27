import os
import uuid
import pandas as pd

from spotipy import SpotifyOAuth, Spotify, CacheHandler, CacheFileHandler
from flask import session, current_app
from datetime import datetime

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
  if not spotify.valid_token():
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
      session['user_choices'] = {} # set up dict for user choices
    if not session.get('display_name'):
      session['display_name'] = None
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

  # get songs to chose from
  def get_songs(self, weather_status=None):
    """Get a possible list of songs based on the weather status

    Args:
        weather_status: String describing the weather

    Returns:
        pandas df: dataframe with track ids/durations in seconds
    """
    if weather_status == "clear":
      genres = ['happy','summer']
    else:
      genres = ['chill', 'rainy-day']
    recs = self.recommendations(
      seed_genres=genres,
      limit=100, 
      max_duration_ms=600000, # at a maximum, have a 10 minute track
      min_popularity=20 # popularity in [0, 100]
    )
    track_list = [(track['id'], track['duration_ms']/1000) for track in recs['tracks']]
    return pd.DataFrame(track_list, columns=['id', 'duration'])

  def curate_songs(self, track_df, length):
    """Curate the songs so that we end up with a list of track ids that are
    close to the time length

    Args:
      track_df: Pandas df of tracks created in get_songs
      length: Desired playlist length in seconds

    Returns:
      list: track ids
    """
    time_remaining = length
    total_time = 0
    chosen_tracks = []
    og_track_df = track_df
    current_track_df = track_df
    
    while time_remaining > 0:
      # if shortest song is longer than the remaining time, we have two options:
      # either end playlist creation there (playlist runs short)
      # or add that song and end playlist creation (playlist runs long)
      # the drive has a sheet with an analysis, and we get closer to the desired length if we run short
      # however, I left the code to have the playlist run long here in case we decide to go with that
      if current_track_df.min(axis=0)['duration'] > time_remaining:
        # UNCOMMENT NEXT 3 LINES TO HAVE PLAYLIST RUN LONG
        # track = current_track_df[current_track_df.duration == current_track_df.duration.min()].iloc[0]
        # chosen_tracks.append(track.id)
        # total_time += track.duration
        time_remaining = 0
      else: # if there's still songs that can fit in the remain time, continue with the function
        # keep only songs that are less than or equal to the time remaining
        current_track_df = current_track_df[current_track_df.duration <= (time_remaining)]
        if current_track_df.empty: # would hit this point if user needed a playlist so long that we need repeats
          current_track_df = og_track_df # will start having repeats
        track = current_track_df.sample().iloc[0]
        current_track_df = current_track_df[current_track_df.id != track.id]
        chosen_tracks.append(track.id)
        total_time += track.duration
        time_remaining = length - total_time
    return chosen_tracks, total_time

  def create_playlist(self, weather_status, duration):
    # find the possible songs df using the weather
    possible_songs_df = self.get_songs(weather_status=weather_status)
    # create a playlist that is close to duration seconds long
    chosen_songs, total_time = self.curate_songs(track_df=possible_songs_df, length=duration)
    new_playlist_name = f'Playlist Maker: {datetime.now().strftime("%D - %H:%M:%S")}'
    user_id = self.me()['id']
    playlist_id = self.user_playlist_create(
      user=user_id,
      name=new_playlist_name
    )['id'] # grab the playlist ID from the json returned with info of the new playlist
    self.user_playlist_add_tracks(user_id, playlist_id, chosen_songs)
    return self.playlist(playlist_id), total_time
