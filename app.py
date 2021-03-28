# app.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__) 

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

    oauth_token = 'TOKEN GOES HERE' # must add auth token here
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

app.run(debug = True)