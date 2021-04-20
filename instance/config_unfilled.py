#### NOTE: Copy this file into the instance folder, rename it config.py, and fill in the keys

# spotify
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback/spotify' # change to domain after deployment
SPOTIFY_SCOPE = 'user-library-read playlist-modify-public playlist-read-collaborative'
SPOTIFY_CACHES_DIR = './.spotify_caches'
# google
GOOGLE_API_KEY = ''
# weather
WEATHER_API_KEY = ''