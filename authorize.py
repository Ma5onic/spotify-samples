import os
import settings
import sys
import logging
import spotipy.util as util

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_token():
    scope = os.getenv('SCOPE')
    username = os.getenv('USERNAME')
    # CLIENT_ID, CLIENT_SECRET, REDIRECT_URI and username are passed as environmental variables
    if os.getenv('TOKEN') == None:
        token = util.prompt_for_user_token(username, scope)
    else:
        return os.getenv('TOKEN')
    logger.info(f'Received token: {token}')
    os.environ['TOKEN'] = token
    return token
