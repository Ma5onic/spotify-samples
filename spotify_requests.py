import spotipy
import json
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_track_by_name(token, artist, track):
    if token:
        sp = spotipy.Spotify(auth=token)
        track_url = sp.search(q='artist:' + artist +
                              ' track:' + track, type='track')
        logger.info(f'Searching for {artist} - {track}')
        try:
            track_url = json.dumps(track_url.get('tracks').get(
                'items')[0].get('external_urls').get('spotify')).replace("\"","")
        except:
            return None
        else:
            return track_url
    else:
        print("No token provided")


def get_currently_playing(token):

    if token:
        sp = spotipy.Spotify(auth=token)
        result = sp.currently_playing()
        # TODO
        # Exception for when not playing anything
        artists = []
        # res = []
        for artist in result.get('item').get('artists'):
            artists.append(artist['name'])
        res = {
            'artists': artists,
            'name': result['item']['name']
        }
        return res
    else:
        print("No token provided")


def get_recently_played_tracks(token):
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_recently_played()
        res = []
        for track in results.get('items'):
            track_name = track.get('track').get('name')
            res.append({
                'artists': [artist.get("name") for artist in track.get('track').get('artists')],
                'name': track_name
            })
        return res
    else:
        print("No token provided")


def get_saved_tracks(token):
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])
    else:
        print("No token provided")


def get_at_favorite(token):
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_top_tracks(limit=50, time_range='long_term')
        res = []
        for item in results['items']:
            res.append({
                'artists': item['artists'][0]['name'],
                'name': item['name']
            })
        return res
    else:
        print("No token provided")
