import authorize
import spotify_requests


def main():
    token = authorize.get_token()
    print(spotify_requests.get_currently_playing(token))


if __name__ == "__main__":
    main()
