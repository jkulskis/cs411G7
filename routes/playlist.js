var express = require('express');
var router = express.Router();
var request = require('request');
const { response } = require('../app');

let tokenOauth2 = 'OAUTH_TOKEN_HERE'

/* GET playlist page. */
router.get('/', function(req, res, next) {
  var options = {
    'method': 'GET',
    'url': 'https://api.spotify.com/v1/playlists/2FHqT8cEwwno145Ds35sdC',
    'headers': {
      'Authorization': `Bearer ${tokenOauth2}`
    },
    'json': true
  };
  request(options, function (error, response) {
    if (error) throw new Error(error);
    data = response.body;
    console.log(data);
    res.render('playlist', { 
      name: data.name, 
      owner: data.owner.display_name,
      numSongs: data.tracks.total,
      playlistImg: data.images[0].url
    });
  });
});

module.exports = router;