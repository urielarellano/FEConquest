import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re
import pprint

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    return BeautifulSoup(resp.text, "html.parser")

wiki_soup = get_soup("https://fireemblem.fandom.com/wiki/List_of_characters_in_Fire_Emblem_Fates")
skills_soup = get_soup("https://serenesforest.net/fire-emblem-fates/nohrian-characters/personal-skills/")
growth_rates_soup = get_soup("https://serenesforest.net/fire-emblem-fates/nohrian-characters/growth-rates/")

data = []

# get wiki data
# includes name, start class, start level, base stats, max stats
# base class, heartseal base, promoted classes, heartseal promoted, sprites
wiki_content = wiki_soup.find("div", class_="mw-content-ltr mw-parser-output")
character_groups = wiki_content.find_all("center")
all_paths_characters = character_groups[0]
conquest_characters = character_groups[2]
izana = character_groups[4]

all_characters = [all_paths_characters, conquest_characters, izana]
hrefs = []
names = []

# fill in hrefs and names
for group in all_characters:
    links = group.find_all("div", class_="link")
    for div in links:
        a_tag = div.find("a")
        if a_tag:
            hrefs.append(a_tag.get("href"))
            names.append(a_tag.text.strip())

wiki_link = "https://fireemblem.fandom.com/"

name_idx = 0 # use names[idx] to get the current character name
for character_wiki in hrefs:
    character_wiki_soup = get_soup(wiki_link + character_wiki + "/Gallery")

for character_wiki in hrefs:
    time.sleep(0.3)
    character_wiki_soup = get_soup(wiki_link + character_wiki)
    
    name = names[name_idx] #✅
    if name == "Laslow":
        character_wiki_soup = get_soup(wiki_link + "wiki/Inigo")
    elif name == "Selena":
        character_wiki_soup = get_soup(wiki_link + "wiki/Severa")
    elif name == "Odin":
        character_wiki_soup = get_soup(wiki_link + "wiki/Owain")
    #####################
    sclass = None #✅
    startLevel = None #✅
    baseStats = {} #✅
    personalSkill = {} #✅
    growthRates = {} #✅
    maxStats = {} #✅
    ####################
    baseClass = None #✅
    heartSealBase = None #✅
    promotedClasses = [] #✅
    heartSealPromoted = [] #✅
    sprites = {} #✅

    # get relevant tables from character wiki
    tables = character_wiki_soup.find_all("table", class_="statbox")
    statbox = tables[0]
    max_stats_table = None
    classes_table = None

    if name == "Laslow" or name == "Selena" or name == "Odin":
        statbox = character_wiki_soup.find("div", class_="tabber wds-tabber").find("table", class_="statbox")
        max_stats_table = character_wiki_soup.find("table", class_="statbox", style="text-align: center")
        # this next line is wrong-- it got the wrong table for all 3 characters and I got some wack ass sprites
        classes_table = character_wiki_soup.find_all("table", class_="statbox", cellpadding="2")[3]
    else:
        for table in tables:
            if table.find("tr", attrs={"bgcolor": "#add8e6"}):
                max_stats_table = table
            elif table.get("cellpadding") == "2":
                classes_table = table
                break
    
    # get character info from statbox
    statbox_rows = statbox.find_all("tr")
    sclass = statbox_rows[1].find_all("a")[1].get("title")
    if name == "Corrin":
        sclass = "Nohr Princess"
    startLevel = statbox_rows[3].find("td").text.strip()
    stats_headers = statbox_rows[2].find_all("a")
    stats = statbox_rows[3].find_all("td")
    for i in range(9):
        baseStats[stats_headers[i+1].text.strip()] = stats[i+1].text.strip()
    

    # get info from max_stats_table
    if name != "Corrin":
        max_stats_rows = max_stats_table.find_all("tr")
        max_headers = max_stats_rows[0].find_all("a")
        max_stats = max_stats_rows[1].find_all("td")
        for i in range(7): #
            maxStats[max_headers[i].text.strip()] = max_stats[i].text.strip()
    else:
        maxStats["Str"] = "0"
        maxStats["Mag"] = "0"
        maxStats["Skl"] = "0"
        maxStats["Spd"] = "0"
        maxStats["Lck"] = "0"
        maxStats["Def"] = "0"
        maxStats["Res"] = "0"


    # get sprite info from classes_table
    classes = classes_table.find_all("td")
    idx = 0
    for td in classes:
        info = td.find_all("a")

        if name == "Azura":
            if idx > 0 and idx < 3:
                idx += 1
                continue
        if name == "Keaton":
            if idx == 2:
                idx += 1
                continue
        if name == "Corrin":
            if idx == 2:
                break

        if name == "Corrin":
            if idx == 0:
                #filename = f"{name}-{info[3].text.strip()}.gif"
                #filepath = os.path.join("assets", "sprites", filename)

                #response = requests.get(info[1].get("href"))
                #if response.status_code == 200:
                #    with open(filepath, "wb") as f:
                #        f.write(response.content)
                sprites[info[3].text.strip()] = info[1].get("href")
                baseClass = info[3].text.strip()
                idx += 1
            else:
                # filename = f"{name}-{info[2].text.strip()}.gif"
                # filepath = os.path.join("assets", "sprites", filename)

                # response = requests.get(info[1].get("href"))
                # if response.status_code == 200:
                #     with open(filepath, "wb") as f:
                #         f.write(response.content)
                sprites[info[2].text.strip()] = info[1].get("href")
                promotedClasses.append(info[2].text.strip())
                idx += 1
                
        else:
            # filename = f"{name}-{info[1].text.strip()}.gif"
            # filepath = os.path.join("assets", "sprites", filename)

            # response = requests.get(info[0].get("href"))
            # if response.status_code == 200:
            #     with open(filepath, "wb") as f:
            #         f.write(response.content)
            sprites[info[1].text.strip()] = info[0].get("href")
            if idx == 0:
                baseClass = info[1].text.strip()
                idx += 1
            elif idx < 3:
                promotedClasses.append(info[1].text.strip())
                idx += 1
            elif idx == 3:
                heartSealBase = info[1].text.strip()
                idx += 1
            else:
                heartSealPromoted.append(info[1].text.strip())
                idx += 1  


    # get info from Serenes personal skills
    if name == "Corrin":
        name = "Avatar"
    tables = skills_soup.find_all("table")
    shared_characters_rows = tables[1].find_all("tr")[1:]
    exclusive_characters_rows = tables[2].find_all("tr")[1:]
    all_rows = shared_characters_rows + exclusive_characters_rows

    for tr in all_rows:
        tds = tr.find_all("td")
        if tds[3].text.strip() == name:
            skillName = tds[1].text.strip()
            description = tds[2].text.strip()
            skillIcon = tds[0].find("img").get("src")
            personalSkill[skillName] = [description, skillIcon]
            break
    name = names[name_idx]
    
    # get info from Serenes Character Growth Rates
    if name == "Corrin":
        name = "Avatar"
    tables = growth_rates_soup.find_all("table")
    shared_characters_rows = tables[3].find_all("tr")
    exclusive_characters_rows = tables[4].find_all("tr")
    headers = shared_characters_rows[0].find_all("th")
    all_rows = shared_characters_rows[1:] + exclusive_characters_rows[1:]
    
    for tr in all_rows:
        tds = tr.find_all("td")
        if tds[0].text.strip() == name:
            for i in range(8):
                growthRates[headers[i+1].text.strip()] = tds[i+1].text.strip()
            break

    name = names[name_idx]
    name_idx +=1
    
    data.append({
        "name": name,
        "class": sclass,
        "startLevel": startLevel,
        "baseStats": baseStats,
        "personalSkill": personalSkill,
        "growthRates": growthRates,
        "maxStats": maxStats,
        "baseClass": baseClass,
        "heartSealBase": heartSealBase,
        "promotedClasses": promotedClasses,
        "heartSealPromoted": heartSealPromoted,
        "sprites": sprites
    })


'''
# replace ’ with ' in data
def clean_quotes(text):
    return text.replace("’", "'").replace("‘", "'")

for entry in data:
    if "personalSkill" in entry:
        for skill, values in entry["personalSkill"].items():
            # Only clean the description (index 1)
            values[0] = clean_quotes(values[0])


# Save to JSON file
with open("characters.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Data saved to characters.json")

'''