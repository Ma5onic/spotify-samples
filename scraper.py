import requests
from bs4 import BeautifulSoup as bs
import json
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_for_track(res):
    # res = json.loads(res)

    logger.info(f'Searching for a track, original request is: {res}')

    artist = res.get('artists')[0]
    song_name = res.get('name').split('(')[0].rstrip()
    URL = f'https://www.whosampled.com/{artist.replace(" ", "-")}/{song_name.replace(" ", "-")}/'
    logger.info(f'Constructed a URL: {URL}')
    return URL

def return_samples(URL):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

    try:
        logger.info(f'Trying to access the URL {URL}')
        page = requests.get(URL, headers=headers)
    except Exception as e:
        logger.info(e)
    else:
        soup = bs(page.content, 'html.parser')

    try:
        section = soup.find('span', text=re.compile('Contains samples of(.*) song(.*)')).find_parent('section')
    except AttributeError as err:
        logger.info('Samples section was not found on the page')
    else:

        sample_entries = section.find_all('div', class_="listEntry sampleEntry")

        results = []

        for sample_entry in sample_entries:
            track_name = sample_entry.find('a', class_='trackName').text.rstrip()
            track_artist = sample_entry.find('span', class_='trackArtist').text.rstrip()
            results.append({
                'track_name': track_name,
                'track_artist': re.sub(r'^by ', '', track_artist).split('(')[0].rstrip()
            })
        results = json.dumps(results, indent=4)
        logger.info(f'Found the following samples: \n {results}')
        return results