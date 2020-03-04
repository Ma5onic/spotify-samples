import os
import settings
import sys
import spotipy.util as util


def get_token():
    scope = 'user-library-read user-read-currently-playing user-read-playback-state'
    username = os.getenv('username')
    # CLIENT_ID, CLIENT_SECRET, REDIRECT_URI and username are passed as environmental variables
    token = util.prompt_for_user_token(username, scope)
    return token
