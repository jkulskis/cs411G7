import os
import spotipy
import uuid
from flask import session

caches_folder = './.spotify_caches/' # where the caches will be stored
if not os.path.exists(caches_folder):
  os.makedirs(caches_folder)

def session_cache_path():
  if not session.get('uuid'):
    session['uuid'] = str(uuid.uuid4()) # Visitor is unknown, give random ID
  return caches_folder + session.get('uuid')

def get_cache_handler():
  return spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())