import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re
from pprint import pprint

def get_soup(url, cache_file=None):
    if cache_file and os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers)
        html = resp.text
        if cache_file:
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(html)
    return BeautifulSoup(html, "html.parser")

data = {} # holds sprite data
data['M-Nohr Prince'] = 'https://static.wikia.nocookie.net/fireemblem/images/1/1b/FE14_Kamui_%28M%29_Dark_Prince_Map_Sprite.gif/revision/latest?cb=20151114124919'
data['F-Nohr Princess'] = 'https://static.wikia.nocookie.net/fireemblem/images/1/17/FE14_Kamui_%28F%29_Dark_Princess_Map_Sprite.gif/revision/latest?cb=20151114124918'
data['M-Nohr Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/0/08/FE14_Kamui_%28M%29_Dark_Blood_Map_Sprite.gif/revision/latest?cb=20151114124919'
data['F-Nohr Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/a/a5/FE14_Kamui_%28F%29_Dark_Blood_Map_Sprite.gif/revision/latest?cb=20151114124918'
data['M-Hoshido Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/c/cb/FE14_Kamui_%28M%29_White_Blood_Map_Sprite.gif/revision/latest?cb=20151114124919'
data['F-Hoshido Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/c/c3/FE14_Kamui_%28F%29_White_Blood_Map_Sprite.gif/revision/latest?cb=20151114124919'


sprites_soup = get_soup('https://fireemblem.fandom.com/wiki/List_of_classes_in_Fire_Emblem_Fates')


tables = sprites_soup.find_all('table')

first_table = tables[0]
#print(str(first_table).splitlines()[0])

for table in tables[1:3]:
    trs = table.find_all('tr')[1:] #skip header row

    for tr in trs:
        tds = tr.find_all('td')

        class_name = tds[1].find('a').text.strip()

        sprites = tds[0].find_all('a')
        if len(sprites) > 1:
            male_sprite = sprites[0].get('href')
            female_sprite = sprites[1].get('href')

            data['M-' + class_name] = male_sprite
            data['F-' + class_name] = female_sprite

        else:
            sprite = sprites[0].get('href')

            prefix_lookup = {
                'Troubadour': lambda: 'F-' if 'F-Troubadour' not in data else 'M-',
                'Maid': lambda: 'F-',
                'Butler': lambda: 'M-',
                'Great Master': lambda: 'M-',
                'Priestess': lambda: 'F-'
            }

            if class_name in prefix_lookup:
                prefix = prefix_lookup[class_name]()
                data[prefix + class_name] = sprite
            else:
                data[class_name] = sprite


# Make folder if it doesn't exist
folder = "default_sprites"
os.makedirs(folder, exist_ok=True)

for key, href in data.items():
    # Get the file extension from the URL
    ext = os.path.splitext(href)[1]  # includes the dot, e.g., ".webp"
    if not ext:  # fallback
        ext = ".webp"
    
    # Build the file path
    filename = f"{key}{ext}"
    filepath = os.path.join(folder, filename)
    
    # Download the image
    response = requests.get(href)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Saved {filename}")
    else:
        print(f"Failed to download {href}")

