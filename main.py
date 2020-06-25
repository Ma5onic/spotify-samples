import authorize
import spotify_requests
import json
import scraper
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    while True:
        if initial_song != current_song:
            initial_song = current_song
            final_dict = {
                'original_track': current_song,
                'samples': get_samples(current_song, token)
            }
            final_dict = json.dumps(final_dict, indent=4)
            logger.info(final_dict)
        else:
            current_song = spotify_requests.get_currently_playing(token)
            time.sleep(1)

def get_samples_from_recently_played(token):
    recently_played_dict = spotify_requests.get_recently_played_tracks(token)
    for track in recently_played_dict:
        final_dict = {
            'original_track': track,
            'samples': get_samples(track, token)
        }
        final_dict = json.dumps(final_dict, indent=4)
        logger.info(final_dict)

def main():
    token = authorize.get_token()

    # Gets samples for currently playing song
    # Other options:
    # tracks_dict = spotify_requests.get_at_favorite(token)
    # tracks_dict = spotify_requests.get_recently_played_tracks(token)
    # tracks_dict = [{'artists': ['J. Cole', 'Kendrick Lamar'],
    #                 'name': 'Forbidden Fruit (feat. Kendrick Lamar)'}]

    # get_samples_from_currently_playing(token)
    get_samples_from_recently_played(token)

if __name__ == "__main__":
    main()
