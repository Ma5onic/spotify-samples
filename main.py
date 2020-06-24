import authorize
import spotify_requests
import json
import scraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_samples(tracks_dict, token):
    for track in tracks_dict:
        URL = scraper.search_for_track(track)
        if scraper.find_samples(URL):
            result = json.loads(scraper.find_samples(URL))
            for res in result:
                track_url = spotify_requests.find_track_by_name(
                    token=token,
                    artist=res.get("track_artist"),
                    track=res.get("track_name"))
                res['track_url'] = str(track_url)
    result = json.dumps(result, indent=4)
    logger.info(f'Found the following samples: \n {result}')
    return result


def main():
    token = authorize.get_token()
    # res = spotify_requests.get_currently_playing(token)
    # res = spotify_requests.get_at_favorite(token)

    # tracks_dict = spotify_requests.get_recently_played_tracks(token)

    tracks_dict = [{'artists': ['J. Cole', 'Kendrick Lamar'],
                    'name': 'Forbidden Fruit (feat. Kendrick Lamar)'}]
    get_samples(tracks_dict, token)


if __name__ == "__main__":
    main()
