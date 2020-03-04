import spotipy
import json


def get_currently_playing(token):

    if token:
        sp = spotipy.Spotify(auth=token)
        result = sp.currently_playing()
        artists = []
        for artist in result['item']['artists']:
            artists.append(artist['name'])
        res = {
            'artists': artists,
            'name': result['item']['name']
        }
        return json.dumps(res)
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
        return json.dumps(res)
    else:
        print("No token provided")
