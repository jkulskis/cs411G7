from pyowm.owm import OWM
import googlemaps
from flask import current_app, session

# grab the origin
def get_weather():
    google_api_key = current_app.config['GOOGLE_API_KEY']
    gmaps = googlemaps.Client(key=google_api_key)

    owm = OWM(current_app.config['WEATHER_API_KEY'])
    mgr = owm.weather_manager()

    origin = session['user_choices']['origin']
    origin_coded = gmaps.geocode(origin)
    origin_lat = origin_coded[0]["geometry"]["location"]["lat"]
    origin_long = origin_coded[0]["geometry"]["location"]["lng"]

    weather = mgr.weather_at_coords(origin_lat, origin_long).weather
    temp = weather.temperature('fahrenheit')["temp"]
    weather_details = weather.detailed_status

    good_weather = ["few", "light", "scattered"]
    if any(x in weather_details.lower() for x in good_weather):
        weather_details = "clear"
    
    return temp, weather_details