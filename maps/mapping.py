from flask import Blueprint, request, render_template, current_app
import googlemaps
# from app import app as app <-- won't work

map_blueprint = Blueprint('map_bp', __name__, template_folder='templates')

# won't work
# with app.app_context():
#     google_api_key = current_app.config['GOOGLE_API_KEY']
#     gmaps = googlemaps.Client(key=google_api_key)

@map_blueprint.route('/form')
def form():
    return render_template('form.html')

@map_blueprint.route('/request', methods=['GET','POST'])
def get_distance():
    google_api_key = current_app.config['GOOGLE_API_KEY']
    gmaps = googlemaps.Client(key=google_api_key)

    origin = request.form['origin']
    destination = request.form['destination']
    mode = request.form['mode']


    data = gmaps.distance_matrix(origin, destination, mode=mode, region='US')
    duration = data["rows"][0]["elements"][0]["duration"]["value"]

    return render_template('display_distance.html', data=data, duration=duration)


