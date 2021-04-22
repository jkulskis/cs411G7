import googlemaps
from pyowm.owm import OWM
from flask import current_app

class Location:
  # TODO: Add error handling for invalid responses (e.g. bad addresses)

  def __init__(self, address=None, init_geo=True):
    self.address = address
    self.geocode = None
    self.lat = None
    self.lon = None
    self.weather = None # pyowm weather object
    self.weather_status = None # custom weather status that we determine with the weather object data
    if self.address and init_geo: # if address supplied, then get the geocode data if init_geo is true
      self.get_geocode_data()
  
  def get_geocode_data(self):
    gmaps = googlemaps.Client(key=current_app.config['GOOGLE_API_KEY'])
    self.geocode = gmaps.geocode(self.address)
    self.lat = self.geocode[0]["geometry"]["location"]["lat"]
    self.lon = self.geocode[0]["geometry"]["location"]["lng"]
  
  def duration_between(self, other, mot):
    """Get the duration between this location and another in seconds, given a 
    mode of transportation (walking, biking, driving)

    Args:
        other (Location): location
        mot (str): mode of transportation
    """
    if not self.address or not other.address: # we need addresses at both locations
      raise AttributeError("Need addresses set for both locations to find duration between")
    gmaps = googlemaps.Client(key=current_app.config['GOOGLE_API_KEY'])
    distance_matrix = gmaps.distance_matrix(self.address, other.address, mode=mot, region='US')
    return distance_matrix["rows"][0]["elements"][0]["duration"]["value"]
  
  # TODO: Better weather status for our data crunching. As of now it is just clear/bad
  def weather_now(self):
    """Grabs the weather for the location, assuming that
    """
    if not self.lat or not self.lon: # we need lat/lon to find the weather at this location
      raise AttributeError("Need to call get_geocode_data or set lat/lon manually")
    owm = OWM(current_app.config['WEATHER_API_KEY'])
    mgr = owm.weather_manager()
    self.weather = mgr.weather_at_coords(self.lat, self.lon).weather
    good_weather = ["few", "light", "scattered"]
    if any(x in self.weather.detailed_status.lower() for x in good_weather):
      self.weather_status = "clear"
    else:
      self.weather_status = "bad"
    return self.weather_status
  
  @property
  def temperature(self):
    if not self.weather: # set the weather attribute by calling weather_now if it is not set
      self.weather_now()
    return self.weather.temperature('fahrenheit')["temp"]