import authorize
import spotify_requests
import json
import scraper


def main():
    token = authorize.get_token()
    # res = spotify_requests.get_currently_playing(token)
    # res = spotify_requests.get_at_favorite(token)

    for res in spotify_requests.get_recently_played_tracks(token):
        URL = scraper.search_for_track(res)
        scraper.return_samples(URL)

if __name__ == "__main__":
    main()
