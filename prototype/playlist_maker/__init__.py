# app.py
from flask import Flask, render_template, request
import requests

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # home route
    @app.route("/") 
    def hello(): # route handler function
        # returning a response
        return render_template('index.html')

    # serving form web page
    @app.route("/playlist")
    def form():
        return render_template('form.html')

    # creating request
    @app.route('/request', methods=['GET','POST'])
    def get_playlist():
        playlist_id = request.form['searchID']
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

        oauth_token = 'BQBOwXg9i3lWs8r2m8sPDqKipA7aMnnyVqGH_rdDCpaKdDUY4LHxD--Cxe7U-AA-AHKWeQFEX11vx1zzrjCze0taqX3SbHrpJcKMf_23Eq7R51XZfqTOgu3EImda8P02-7-gHAdIJmLW1hpaw2ApJWo2z8TLk1p9lHlSFHb25aTq67HarlXvoJ450Dw9rWX0_CB9IQ9HajVL' # must add auth token here
        payload={}
        headers = {
        'Authorization': f'Bearer {oauth_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()

        return render_template('display_playlist.html', 
        name = data['name'],
        owner = data['owner']['display_name'],
        num_songs = data['tracks']['total'],
        playlist_image = data['images'][0]['url'])
    return app