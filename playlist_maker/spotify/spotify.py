import os
import uuid

from spotipy import SpotifyOAuth, Spotify, CacheHandler, CacheFileHandler
from flask import session, current_app
# from spomato import spomato
import pandas as pd

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

  # def create_spomato(self):
  #   spomato = spomato.Spomato(access_token=self.get_cache_handler().get_cached_token())
  #   return spomato

  def valid_token(self):
    """Returns true if the oauth token is valid, false otherwise
    """
    if not self.auth_manager.validate_token(self.get_cache_handler().get_cached_token()):
      return False
    return True

  # get songs to chose from
  def get_songs(self, weather_details):
    if weather_details.lower() == "clear":
      genres = ['happy','summer']
    else:
      genres = ['chill', 'rainy-day']
    # if speed == "slower":
    #   energy = 0.3
    # elif speed == "normal":
    #   energy = 0.5
    # else:
    #   energy = 0.7
    recs = self.recommendations(seed_genres=genres,limit=5, max_duration_ms=360000, min_popularity=50)

    track_list = []
    tracks = recs['tracks']
    for track in tracks:
      track_id = track['id']
      duration = track['duration_ms']/1000
      track_list.append([track_id, duration])
      # could add filtering by market too

    track_df = pd.DataFrame(track_list, columns=['id','duration'])
    return track_df

  def curate_songs(self,track_df,length):
    time_remaining = length
    total_time = 0
    chosen_tracks = []
    og_track_df = track_df
    current_track_df = track_df
    
    while (time_remaining > 0):
      # if shortest song is longer than the remaining time, end playlist creation
      # because we've gotten as close as we can get to the desired playlist length
      # however, this will make the playlist slightly shorter than the desired length
      # and we could change the logic where we append this short song at the end
      # and have the playlist always be slightly longer than desired
      if current_track_df.min(axis=0)['duration'] > time_remaining:
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

  def create_playlist(self, user_id, chosen_songs):
    new_playlist_name = 'sample'
    self.user_playlist_create(user=user_id, name=new_playlist_name)
    playlists = self.user_playlists(user_id)
    for playlist in playlists['items']:
      if playlist['name'] == new_playlist_name:
        playlist_id = playlist['id']
    self.user_playlist_add_tracks(user_id, playlist_id, chosen_songs)
    return self.playlist(playlist_id)

