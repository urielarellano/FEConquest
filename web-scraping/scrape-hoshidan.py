import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    return BeautifulSoup(resp.text, "html.parser")

url_max_stats = "https://serenesforest.net/fire-emblem-fates/hoshidan-classes/maximum-stats/"
url_mov = "https://serenesforest.net/fire-emblem-fates/hoshidan-classes/base-stats/"
url_skills = "https://serenesforest.net/fire-emblem-fates/hoshidan-classes/class-skills/"
url_growth_rates = "https://serenesforest.net/fire-emblem-fates/hoshidan-classes/growth-rates/"

data = []

# append class name, weapons, classMaxStats (except Mov)
soup = get_soup(url_max_stats)
entry_div = soup.find("div", class_="entry")
table = entry_div.find_all("table")[1]
headers = table.find_all("th")
entries = table.find_all("tr")

for tr in entries:
    class_data = tr.find_all("td")
    # get Class Name
    if class_data:
        className = class_data[0].text.strip()
    else:
        continue
    weapons = {}
    maxStats = {}

    # get Weapon Data
    weapon_entries = class_data[9].find_all("a")
    for a in weapon_entries:
        weaponTitle = a.find("img").get("title")

        weaponRank = a.next_sibling
        if weaponRank is None:
            weaponRank = a.parent.next_sibling
        match = re.search(r'[BAS]', str(weaponRank).upper())
        weaponRank = match.group(0) if match else ""

        weapons[weaponTitle] = weaponRank

    # get Max Stats
    for i in range(8):
        maxStats[headers[i+1].text.strip()] = class_data[i+1].text.strip()

    data.append({
        "class": className,
        "weapons": weapons,
        "skills": {},
        "classGrowthRates": {},
        "classMaxStats": maxStats
    })


# add classGrowthRates
soup = get_soup(url_growth_rates)
entry_div = soup.find("div", class_="entry")
table = entry_div.find_all("table")[1]
headers = table.find_all("th")
entries = table.find_all("tr")

idx = 0
for tr in entries:
    class_data = tr.find_all("td")
    if class_data:
        growthRates = {}
        for i in range(8):
            growthRates[headers[i+1].text.strip()] = class_data[i+1].text.strip()
        data[idx]["classGrowthRates"] = growthRates
        idx += 1


# append Mov to each classMaxStats
soup = get_soup(url_mov)
entry_div = soup.find("div", class_="entry")
table = entry_div.find_all("table")[1]
mov_header = table.find_all("th")[9].text.strip()
entries = table.find_all("tr")

idx = 0
for tr in entries:
    class_data = tr.find_all("td")
    if class_data:
        # do the stuff
        data[idx]["classMaxStats"][mov_header] = class_data[9].text.strip()
        idx += 1


# add classSkills
soup = get_soup(url_skills)
entry_div = soup.find("div", class_="entry")
table = entry_div.find_all("table")[1]
entries = table.find_all("tr")

idx = 0
skip = False # skip current tr if it is True
for tr in entries:
    class_data = tr.find_all("td")
    
    if class_data:
        if skip is False:
            print(class_data[3].text.strip())
            skillName = class_data[1].text.strip()
            level = class_data[4].text.strip()
            description = class_data[2].text.strip()
            skill_url = class_data[0].find("img").get("src")

            # get info for the next skill
            next_tr = tr.find_next_sibling("tr")
            class_data = next_tr.find_all("td")
            second_skillName = class_data[1].text.strip()
            second_level = class_data[4].text.strip()
            second_description = class_data[2].text.strip()
            second_skill_url = class_data[0].find("img").get("src")

            # get info for the next next next skill if class is Troubadour
            if class_data[3].text.strip() == "Songstress":
                third_tr = next_tr.find_next_sibling("tr")
                class_data = third_tr.find_all("td")
                third_skillName = class_data[1].text.strip()
                third_level = class_data[4].text.strip()
                third_description = class_data[2].text.strip()
                third_skill_url = class_data[0].find("img").get("src")

                fourth_tr = third_tr.find_next_sibling("tr")
                class_data = fourth_tr.find_all("td")
                fourth_skillName = class_data[1].text.strip()
                fourth_level = class_data[4].text.strip()
                fourth_description = class_data[2].text.strip()
                fourth_skill_url = class_data[0].find("img").get("src")
                
                data[idx]["skills"] = {
                    skillName: [level, description, skill_url],
                    second_skillName: [second_level, second_description, second_skill_url],
                    third_skillName: [third_level, third_description, third_skill_url],
                    fourth_skillName: [fourth_level, fourth_description, fourth_skill_url]
                }
            else:
                data[idx]["skills"] = {
                    skillName: [level, description, skill_url],
                    second_skillName: [second_level, second_description, second_skill_url]
                }
            skip = True
            idx += 1
            print(class_data[3].text.strip() + "merp")
            
        else:
            if class_data[1].text.strip() == "Inspiring Song":
                continue
            if class_data[1].text.strip() == "Voice of Peace":
                continue
            skip = False
        


'''
for entry in data:
    if entry["class"] == "Nohr Prince(ss)":
        print(json.dumps(entry, indent=4))
        break  # Optional: stop after the first match
'''

#print(json.dumps(data, indent=4))

'''
for a in portrait_links:
    name = a.get("data-title", "Unknown").strip()
    img_url = a.get("href")
    if not name or not img_url:
        continue
    if name == "Flora":
        break
    data.append({
        "name": name,
        "image_url": img_url
    })
'''

# replace ’ with ' in data
def clean_quotes(text):
    return text.replace("’", "'").replace("‘", "'")

for entry in data:
    if "skills" in entry:
        for skill, values in entry["skills"].items():
            # Only clean the description (index 1)
            values[1] = clean_quotes(values[1])


# Save to JSON file
with open("hoshidan-classes.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Data saved to hoshidan-classes.json")
