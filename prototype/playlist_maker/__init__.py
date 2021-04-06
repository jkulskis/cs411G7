# app.py
from flask import Flask, render_template, request
import requests

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    ''' app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass '''

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
    
    from . import auth
    app.register_blueprint(auth.auth_bp)

    return app