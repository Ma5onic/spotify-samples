from flask import Flask
import spotify_requests
import authorize
import scraper
import json
import logging
import os
from flask_cors import CORS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
token = authorize.get_token()


def get_samples(tracks_dict, token):

    URL = scraper.search_for_track(tracks_dict)
    found_samples = scraper.find_samples(URL)
    if found_samples:
        result = json.loads(found_samples['results'])
        for res in result:
            sample_url_in_spotify = spotify_requests.find_track_by_name(
                token=token,
                artist=res.get("track_artist"),
                track=res.get("track_name"))
            res['track_url'] = sample_url_in_spotify
        logger.info(f'Found the following samples: \n {result}')
        return {
            'samples': result,
            'whosampled_url': found_samples['URL']
        }
    else:
        return {
            'samples': None,
            'whosampled_url': None
        }


def get_samples_from_currently_playing(token):
    current_song = spotify_requests.get_currently_playing(token)
    samples = get_samples(current_song, token)
    if current_song:
        final_dict = {
            'original_track': current_song,
            'whosampled_url': samples.get('whosampled_url'),
            'samples': samples.get('samples'),
        }
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


def get_samples_from_playlist(username, playlist_id, token):
    tracks_in_playlist = spotify_requests.get_playlist_tracks(
        username, playlist_id, token)
    res = {
        'results': []
    }
    for track in tracks_in_playlist:
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


@app.route("/api/playlist/<playlist_id>")
def tracks_from_playlist(playlist_id):
    response = spotify_requests.get_playlist_tracks(
        os.getenv('USERNAME'), playlist_id, token)
    return json.dumps(response)


@app.route("/api/playlist/<playlist_id>/samples")
def samples_from_playlist(playlist_id):
    response = get_samples_from_playlist(
        os.getenv('USERNAME'), playlist_id, token)
    return json.dumps(response)
