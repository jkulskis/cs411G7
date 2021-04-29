# cs411G7

## Backend to Frontend Mapping
1. home > `home.py` == `Home.js`
    * Already handled
2. travel > `travel.py` == `Page1.js`
    * Variables in `travel.py` to grab from the backend when making a `GET` request from the frontend to the backend:
        * '**display_name**' == The username
        * '**user_choices**' == At this point, this stores the user's origin and destination
    * Variables that should exist in `Page1.js` to send to the backend when making a `POST` request from the frontend to the backend:
        * '**origin**' == User's current location. In `travel.py`, this will be used the line `origin = request.args.get('origin')`
        * '**destination**' == User's destination. In `travel.py`, this will be used the line `destination = request.args.get('destination')`

3. mot > `mot.py` == `Page2.js`
    * Variables in `mot.py` to grab from the backend when making a `GET` request from the frontend to the backend:
        * '**display_name**' == The username
        * '**user_choices**' == At this point, this stores the user's origin, destination, and mode of transportation
    * Variables that should exist in `Page2.js` to send to the backend when making a `POST` request from the frontend to the backend:
        * '**mot**' == The user's mode of transportation. In `mot.py`, this will be used in the line `mot = request.args.get('mot')`. Value of '**mot**' should either be 'walking', 'driving', or 'biking'
4. speed > `speed.py` == `Page3.js`
    * Variables in `speed.py` to grab from the backend when making a `GET` request from the frontend to the backend:
        * '**display_name**' == The username
        * '**user_choices**' == At this point, this stores the user's origin, destination, mode of transportation, and speed
    * Variables that should exist in `Page3.js` to send to the backend when making a `POST` request from the frontend to the backend:
        * '**speed**' == The user's speed. In `speed.py`, this will be used in the line `speed = request.args.get('speed')`. Value of '**speed**' should either be 'slower', 'normal', or 'faster'
5. playlist > `playlist.py` == `Page4.js`
    * Variables in `mot.py` to grab from the backend when making a `GET` request from the frontend to the backend:
        * '**display_name**' == The username
        * '**user_choices**' == This stores the user's origin, destination, mode of transportation, and speed
        * '**playlist**' == The URL of the playlist. Clicking the "My Playlist" button should show this
    * No `POST` requests necessary

