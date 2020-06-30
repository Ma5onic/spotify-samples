import spotify_requests
from flask import Flask
from flask_restful import Resource, Api
import logging
import authorize
import scraper
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app, prefix="/api")

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
    final_dict = {
        'original_track': current_song,
        'samples': get_samples(current_song, token)
    }
    final_dict = final_dict
    logger.info(f'Heres the final dict {final_dict}, {type(final_dict)}')
    return(final_dict)

class CurrentlyPlaying(Resource):
    def get(self):
        response = spotify_requests.get_currently_playing(token)
        return response

class RecentlyPlayed(Resource):
    def get(self):
        response = spotify_requests.get_recently_played_tracks(token)
        return response

class SamplesFromCurrentlyPlaying(Resource):
    def get(self):
        response = get_samples_from_currently_playing(token)
        return response

api.add_resource(CurrentlyPlaying, '/currently-playing')
api.add_resource(RecentlyPlayed, '/recently-played')
api.add_resource(SamplesFromCurrentlyPlaying, '/currently-playing/samples')

if __name__ == '__main__':
    app.run(debug=True)