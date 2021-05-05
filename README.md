# cs411G7
Repo for Spring 2021 CS411 Final Project.
## Team
Group 7, Section A3:
* John Mikulskis: *jkulskis*
* Chloe Adamowicz: *chloeadamo*
* Hannah Barenboim: *hannahb323*
* Akash Rudra: *akashrudra18*
* Jamie Dela Cruz: *jamie-dc* and *aahwangxyz* (Jamie's note: As stated on a private Piazza post, I had technical problems with my laptop halfway through the semester, so I borrowed a friend's laptop. Despite logging into my GitHub account on their device, it somehow still pushed to the repo using their account. However, all changes are made from *aahwangxyz* are entirely mine.)

## Demo Video
Please see the video at https://drive.google.com/file/d/1oTneTqdWQeWO4RuM6fG7VV4ioJOKsJ3b/view?usp=sharing for a walkthrough of our web app. 

## Project Summary
Want the perfect playlist for your commute, a bike ride, or a walk outside? Our **Playlist Maker** web application creates a customized playlist for your travel needs. Just input your current location and destination, your mode of transportation, and the speed of your travel (in a rush? taking your time? or just going at a regular pace?). Our app calculates the length of your commute and generates a playlist with a duration that closely matches so that you don't have to do that fiddling yourself. But that's not all! We know that you don't want to listen to bright and cheery music when it's gloomy out, and you don't want to bring the mood down when the sun is shining. Our app also matches the music to the current weather, creating a playlist custom-made for the exact trip you're about to take. 

## Technical Requirements
* Utilizes a redis database.
* Two APIs:
    - Weather: [Open Weather Map API](https://openweathermap.org/api) to grab the current weather. This information is factored in when choosing the music genres for generating the playlist. We used the [PyOWM](https://pyowm.readthedocs.io/en/latest/) Python wrapper library in implementation.
    - Spotify: [Spotify Web API](https://developer.spotify.com/documentation/web-api/) to generate the playlist for the user. We used the [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/) Python library in implementation.
* Third party authentication:
    - Logging into Spotify with [User Authorization](https://developer.spotify.com/documentation/general/guides/authorization-guide/) with OAuth 2.0
* Decoupled Architecture:
    - Python Flask backend, React frontend.

## Extras
* Google Maps [Geocoding API](https://developers.google.com/maps/documentation/geocoding/start) to get the latitude and longitude of a given location and Google Maps [Distance Matrix](https://developers.google.com/maps/documentation/distance-matrix/overview) to calculate the commute time between the origin and destination. We used the [googlemaps](https://github.com/googlemaps/google-maps-services-python) Python library in implementation.