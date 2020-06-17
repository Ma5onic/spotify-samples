import requests
from bs4 import BeautifulSoup as bs
import json
import re

def search_for_track():
    return

def return_samples(URL):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

    page = requests.get(URL, headers=headers)
    soup = bs(page.content, 'html.parser')

    section = soup.find('span', text='Contains samples of 3 songs').find_parent('section')

    sample_entries = section.find_all('div', class_="listEntry sampleEntry")

    results = []

    for sample_entry in sample_entries:
        results.append({
            'track_name': sample_entry.find('a', class_='trackName').text,
            'track_artist': re.sub(r'^by ', '', sample_entry.find('span', class_='trackArtist').text)
            })

    return json.dumps(results, indent=4)

URL = 'https://www.whosampled.com/J.-Cole/Forbidden-Fruit/'

print(return_samples(URL))