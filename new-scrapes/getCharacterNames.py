import requests
from bs4 import BeautifulSoup
import os

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


def get_character_names():
    character_list_soup = get_soup("https://fireemblem.fandom.com/wiki/List_of_characters_in_Fire_Emblem_Fates")
    wiki_content = character_list_soup.find("div", class_="mw-content-ltr mw-parser-output")
    character_groups = wiki_content.find_all("center")

    # get each center div with characters
    all_paths_characters = character_groups[0]
    conquest_characters = character_groups[2]
    izana = character_groups[4]
    all_paths_children = character_groups[6]
    conquest_children = character_groups[8]

    all_characters = [all_paths_characters, conquest_characters, izana, all_paths_children, conquest_children]

    names = []
    # loop through all center divs
    for character_group in all_characters:
        character_link_divs = character_group.find_all("div", class_="link")

        for div in character_link_divs:
            a_tag = div.find("a")
            if a_tag.text.strip() == 'Kana':
                names.append('Kana M')
                names.append('Kana F')
            else:
                names.append(a_tag.text.strip())

    return names

def get_birthright_names():
    character_list_soup = get_soup("https://fireemblem.fandom.com/wiki/List_of_characters_in_Fire_Emblem_Fates")
    wiki_content = character_list_soup.find("div", class_="mw-content-ltr mw-parser-output")
    character_groups = wiki_content.find_all("center")

    birthright_characters = character_groups[1]
    yukimura = character_groups[3]
    fuga = character_groups[5]
    birthright_children = character_groups[7]

    all_characters = [birthright_characters, yukimura, fuga, birthright_children]
    
    names = []
    # loop through all center divs
    for character_group in all_characters:
        character_link_divs = character_group.find_all("div", class_="link")

        for div in character_link_divs:
            a_tag = div.find("a")
            names.append(a_tag.text.strip())

    return names


names = [
    "Corrin",
    "Azura",
    "Felicia",
    "Jakob",
    "Silas",
    "Kaze",
    "Mozu",
    "Shura",
    "Xander",
    "Camilla",
    "Leo",
    "Elise",
    "Laslow",
    "Peri",
    "Selena",
    "Beruka",
    "Odin",
    "Niles",
    "Effie",
    "Arthur",
    "Nyx",
    "Charlotte",
    "Benny",
    "Keaton",
    "Gunter",
    "Flora",
    "Izana",
    "Kana M",
    "Kana F",
    "Shigure",
    "Dwyer",
    "Sophie",
    "Midori",
    "Siegbert",
    "Forrest",
    "Soleil",
    "Ophelia",
    "Nina",
    "Percy",
    "Ignatius",
    "Velouria",
]