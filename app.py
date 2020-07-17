# import authorize
# import spotify_requests
# import json
# import scraper
# import time

# from flask import Flask
# from flask_restful import Resource, Api


# app = Flask(__name__)
# api = Api(app, prefix="/api")
# api.add_resource(views.CurrentlyPlaying, '/currently-playing')
# api.add_resource(views.RecentlyPlayed, '/recently-played')
# api.add_resource(views.SamplesFromCurrentlyPlaying, '/currently-playing/samples')
# api.add_resource(views.HomePage, '/')

# app.run(debug=True)

from flask import Flask
import spotify_requests
import authorize
import scraper
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

token = authorize.get_token()

def get_samples(tracks_dict, token):

    URL = scraper.search_for_track(tracks_dict)
    found_samples = scraper.find_samples(URL)
    if found_samples:
        result = json.loads(found_samples)
        for res in result:
            sample_url = spotify_requests.find_track_by_name(
                token=token,
                artist=res.get("track_artist"),
                track=res.get("track_name"))
            res['track_url'] = sample_url
        logger.info(f'Found the following samples: \n {result}')
        return result

def get_samples_from_currently_playing(token):
    initial_song = None
    current_song = spotify_requests.get_currently_playing(token)
    if current_song:
        final_dict = {
            'original_track': current_song,
            'samples': get_samples(current_song, token)
        }
        final_dict = final_dict
        return(final_dict)
    else:
        return None


def get_samples_from_recently_played(token):
    recently_played_dict = spotify_requests.get_recently_played_tracks(token)
    res = {
        'results': []
    }
    for track in recently_played_dict:
        final_dict = {
            'original_track': track,
            'samples': get_samples(track, token)
        }
        logger.info(json.dumps(final_dict, indent=4))
        res['results'].append(final_dict)
    return res

@app.route("/")
def hello():
    return "Welcome to Spotify Samples app"

@app.route("/api/currently-playing")
def currently_playing():
    response = spotify_requests.get_currently_playing(token)
    return response

@app.route("/api/currently-playing/samples")
def samples_from_currently_playing():
    response = get_samples_from_currently_playing(token)
    return response

@app.route("/api/recently-played/samples")
def samples_from_recently_played():
    response = get_samples_from_recently_played(token)
    return response