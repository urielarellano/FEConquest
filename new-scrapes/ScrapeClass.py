import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re
from pprint import pprint

from getCharacterNames import get_character_names
from getCharacterNames import get_birthright_names


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


################## Character class ####################
class Character:
    CHILD_NAMES = [
        "Kana M", "Kana F", "Shigure", "Dwyer", "Sophie", "Midori",
        "Siegbert", "Forrest", "Soleil", "Ophelia", "Nina",
        "Percy", "Ignatius", "Velouria",
    ]
    GENDER_DATA = {
        "Corrin": "F", "Azura": "F", "Felicia": "F", "Jakob": "M",
        "Silas": "M", "Kaze": "M", "Mozu": "F", "Shura": "M", "Xander": "M",
        "Camilla": "F", "Leo": "M", "Elise": "F", "Laslow": "M", "Peri": "F",
        "Selena": "F", "Beruka": "F", "Odin": "M", "Niles": "M", "Effie": "F",
        "Arthur": "M", "Nyx": "F", "Charlotte": "F", "Benny": "M", "Keaton": "M",
        "Gunter": "M", "Flora": "F", "Izana": "M", "Kana M": "M", "Kana F": "F",
        "Shigure": "M", "Dwyer": "M", "Sophie": "F", "Midori": "F", 
        "Siegbert": "M", "Forrest": "M", "Soleil": "F", "Ophelia": "F", 
        "Nina": "F", "Percy": "M", "Ignatius": "M", "Velouria": "F",
    }
    BIRTHRIGHT_CHARACTERS = set(get_birthright_names())
    SKILLS_SOUP = get_soup("https://serenesforest.net/fire-emblem-fates/nohrian-characters/personal-skills/")
    GROWTH_RATES_SOUP = get_soup("https://serenesforest.net/fire-emblem-fates/nohrian-characters/growth-rates/")
    MAX_STATS_SOUP = get_soup("https://serenesforest.net/fire-emblem-fates/nohrian-characters/maximum-stats/")

    def __init__(self, name: str):
        self.name = name
        self.gender = self.GENDER_DATA[name]
        self.is_child = name in Character.CHILD_NAMES

        self.fathers: list[str] = []
        self.mothers: list[str] = []
        self.starting_class: str = ""
        self.start_level: str = ""
        self.base_stats: dict[str, str] = {}

        self.personal_skill: dict[str, list[str]] = {}
        self.growth_rates: dict[str, str] = {}
        self.max_stats: dict[str, str] = {}

        self.base_class: list[str] = []
        self.heart_sets: dict[str, list[str]] = {}
        self.partner_sets: dict[str, list[str]] = {}
        self.buddy_sets: dict[str, list[str]] = {}

        self.sprites: dict[str, str] = {}
        # Inigo, Severa, Owain
        if name == "Laslow":
            self.wiki_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Inigo")
            #self.gallery_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Inigo/" + "Gallery")
        elif name == "Selena":
            self.wiki_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Severa")
            #self.gallery_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Severa/" + "Gallery")
        elif name == "Odin":
            self.wiki_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Owain")
            #self.gallery_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Owain/" + "Gallery")
        elif name == "Arthur":
            self.wiki_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Arthur_(Fates)")
        elif name == "Ignatius":
            self.wiki_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Ignatius_(Fates)")
        elif name == "Kana M" or name == "Kana F":
            self.wiki_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + "Kana")
        else:
            self.wiki_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + name)
            #self.gallery_soup: BeautifulSoup = get_soup("https://fireemblem.fandom.com/" + name + "/Gallery")

    #################### functions ###########################
    # helper function because Ignatius statbox is not on the wiki
    def populate_ignatius_statbox(self):
        """
        Populate Ignatius starting_class, start_level, and base_stats
        """
        self.starting_class = 'Knight'
        self.start_level = '14'
        self.base_stats['HP'] = '8'
        self.base_stats['Str'] = '7'
        self.base_stats['Mag'] = '0'
        self.base_stats['Skl'] = '6'
        self.base_stats['Spd'] = '4'
        self.base_stats['Lck'] = '7'
        self.base_stats['Def'] = '6'
        self.base_stats['Res'] = '7'
        self.base_stats['Mov'] = '4'

        return None

    # get statbox from wiki_soup and populate variables
    def populate_statbox_info(self):
        """
        Populate starting_class, start_level, and base_stats
        by parsing the statbox from the wiki_soup object
        """
        if self.name == "Laslow" or self.name == "Selena" or self.name == "Odin":
            statbox = self.wiki_soup.find("div", class_="tabber wds-tabber").find("table", class_="statbox")
        elif self.name == "Ignatius":
            self.populate_ignatius_statbox()
            return None
        else:
            statbox = self.wiki_soup.find("table", class_="statbox")


        statbox_rows = statbox.find_all("tr")
        # set starting_class
        self.starting_class = statbox_rows[1].find_all("a")[1].get("title")
        if self.name == "Corrin":
            self.starting_class = "Nohr Princess"
        if self.name == "Leo":
            self.starting_class = "Dark Knight"

        # set start_level
        self.start_level = statbox_rows[3].find("td").text.strip()
        if self.name == "Soleil":
            self.start_level = '10'

        # set base_stats
        stats_headers = statbox_rows[2].find_all("a")
        stats = statbox_rows[3].find_all("td")

        for i in range(9):
            # Sophie specific case
            if self.name == "Sophie" and i == 5:
                self.base_stats['Lck'] = '10'
            if self.name == "Sophie" and i == 8:
                continue
            # Soleil specific case
            if self.name == "Soleil":
                self.base_stats[stats_headers[i].text.strip()] = stats[i].text.strip()
                continue
            # Ophelia specific case
            if self.name == "Ophelia" and i == 8:
                self.base_stats['Mov'] = '5'
                continue

            self.base_stats[stats_headers[i+1].text.strip()] = stats[i+1].text.strip()

        return None
    
    # set personal skill using serenes skills soup
    def set_personal_skill(self):
        """
        set personal_skill by parsing SKILLS_SOUP
        """
        # get every personal skill row
        trs = self.SKILLS_SOUP.find_all("tr")

        # find the row of self.name
        for tr in trs:
            td = tr.find("td", string=self.name)
            if self.name == 'Corrin':
                td = tr.find('td', string='Avatar')
            if td:
                tds = tr.find_all('td')
                # fill in personal skill name, description, and icon url
                self.personal_skill[tds[1].text.strip()] =[tds[2].text.strip(), tds[0].find("img").get("src")]
                break
        
        return None
    
    # set growth rates using serenes growth rates soup
    def set_growth_rates(self):
        """
        Set growth_rates by parsing GROWTH_RATES_SOUP
        """
        # get all rows
        trs = self.GROWTH_RATES_SOUP.find_all("tr")

        # get the stat headers (HP, Str, etc)
        stat_headers = None
        for tr in trs:
            th = tr.find("th", string='Name')
            if th:
                stat_headers = tr.find_all('th')
                break

        # find the current character's row (their stats)
        for tr in trs:
            td = tr.find("td", string=self.name)
            if self.name == 'Corrin':
                td = tr.find('td', string='Avatar')
            if td:
                for i in range(8):
                    tds = tr.find_all('td')
                    self.growth_rates[stat_headers[i+1].text.strip()] = tds[i+1].text.strip()
                break
        
        return None
    
    # set max stats using serenes max stats soup
    def set_max_stats(self):
        """
        Set growth rates by parsing MAX_STATS_SOUP
        """
        # get all rows
        trs = self.MAX_STATS_SOUP.find_all("tr")

        # get the stat headers (HP, Str, etc)
        stat_headers = None
        for tr in trs:
            th = tr.find("th", string='Name')
            if th:
                stat_headers = tr.find_all('th')
                break

        # find the current character's row (their stats)
        for tr in trs:
            td = tr.find("td", string=self.name)
            if td:
                for i in range(7):
                    tds = tr.find_all('td')
                    stat_value = tds[i+1].text.strip()
                    # append '+' to start of positive stat_values
                    if stat_value.isdigit():
                        stat_value = f"+{stat_value}"
                    # make blank values = '0'
                    if stat_value == '':
                        stat_value = '0'
                    
                    self.max_stats[stat_headers[i+1].text.strip()] = stat_value
                break

        # set child max_stats
        if self.is_child:
            for i in range(7):
                self.max_stats[stat_headers[i+1].text.strip()] = '+1'
        
        # set Corrin max_stats
        if self.name == 'Corrin':
            for i in range(7):
                self.max_stats[stat_headers[i+1].text.strip()] = '0'

        return None
    
    
    #################### set classes ########################
    # helper function to set Corrin's classes using wiki_soup
    def _set_corrin_classes(self):
        """
        manually set Corrin's base and heart classes
        """

        # base class and sprites
        self.base_class = ['Nohr Princess', 'Nohr Noble', 'Hoshido Noble']
        self.sprites['Nohr Princess'] = 'https://static.wikia.nocookie.net/fireemblem/images/1/17/FE14_Kamui_%28F%29_Dark_Princess_Map_Sprite.gif/revision/latest?cb=20151114124918'
        self.sprites['Nohr Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/a/a5/FE14_Kamui_%28F%29_Dark_Blood_Map_Sprite.gif/revision/latest?cb=20151114124918'
        self.sprites['Hoshido Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/c/c3/FE14_Kamui_%28F%29_White_Blood_Map_Sprite.gif/revision/latest?cb=20151114124919'

        # heart classes
        self.heart_sets['Archer'] = ['Archer', 'Sniper', 'Kinshi Knight']
        self.heart_sets['Cavalier'] = ['Cavalier', 'Paladin', 'Great Knight']
        self.heart_sets['Dark Mage'] = ['Dark Mage', 'Sorcerer', 'Dark Knight']
        self.heart_sets['Fighter'] = ['Fighter', 'Berserker', 'Hero']
        self.heart_sets['Apothecary'] = ['Apothecary', 'Mechanist', 'Merchant']
        self.heart_sets['Knight'] = ['Knight', 'General', 'Great Knight']
        self.heart_sets['Spear Fighter'] = ['Spear Fighter', 'Spear Master', 'Basara']
        self.heart_sets['Mercenary'] = ['Mercenary', 'Hero', 'Bow Knight']
        self.heart_sets['Ninja'] = ['Ninja', 'Master Ninja', 'Mechanist']
        self.heart_sets['Oni Savage'] = ['Oni Savage', 'Oni Chieftain', 'Blacksmith']
        self.heart_sets['Outlaw'] = ['Outlaw', 'Adventurer', 'Bow Knight']
        self.heart_sets['Sky Knight'] = ['Sky Knight', 'Falcon Knight', 'Kinshi Knight']
        self.heart_sets['Troubadour'] = ['Troubadour', 'Maid', 'Strategist']
        self.heart_sets['Shrine Maiden'] = ['Shrine Maiden', 'Priestess', 'Onmyoji']
        self.heart_sets['Samurai'] = ['Samurai', 'Swordmaster', 'Master of Arms']
        self.heart_sets['Diviner'] = ['Diviner', 'Onmyoji', 'Basara']
        self.heart_sets['Wyvern Rider'] = ['Wyvern Rider', 'Wyvern Lord', 'Malig Knight']

        return None

    # helper function to set Kana's classes using wiki_soup
    def _set_kana_classes(self):
        """
        set Kana's base, heart, partner and buddy classes
        and fathers/mothers
        """

        # male Kana spans
        mother_span_one = self.wiki_soup.find('span', id='Inheritance_from_Mother')
        father_span_one = self.wiki_soup.find('span', id='Inheritance_from_Father')
        buddy_span_one = self.wiki_soup.find('span', id='Buddy_Sets')
        partner_span_one = self.wiki_soup.find('span', id='Marriage_Sets')

        # female Kana spans
        mother_span_two = self.wiki_soup.find('span', id='Inheritance_from_Mother_2')
        father_span_two = self.wiki_soup.find('span', id='Inheritance_from_Father_2')
        buddy_span_two = self.wiki_soup.find('span', id='Friendship_Sets')
        partner_span_two = self.wiki_soup.find('span', id='Partner_Sets')


        if self.name == 'Kana M':
            self.base_class = ['Nohr Prince', 'Nohr Noble', 'Hoshido Noble']
            self.sprites['Nohr Prince'] = 'https://static.wikia.nocookie.net/fireemblem/images/3/39/FE14_Kanna_%28M%29_Nohr_Prince_Map_Sprite.gif/revision/latest?cb=20160210044859'
            self.sprites['Nohr Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/c/c6/FE14_Kanna_%28M%29_Dark_Blood_Map_Sprite.gif/revision/latest?cb=20160210044859'
            self.sprites['Hoshido Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/3/34/FE14_Kanna_%28M%29_White_Blood_Map_Sprite.gif/revision/latest?cb=20160210044859'

            self._set_classes_from_span(mother_span_one, 'heart', False)
            self._set_classes_from_span(father_span_one, 'heart', True)
            self._set_classes_from_span(buddy_span_one, 'buddy', False)
            self._set_classes_from_span(partner_span_one, 'partner', False)
        else:
            # get classes for female Kana
            self.base_class = ['Nohr Princess', 'Nohr Noble', 'Hoshido Noble']
            self.sprites['Nohr Princess'] = 'https://static.wikia.nocookie.net/fireemblem/images/8/86/FE14_Kanna_%28F%29_Nohr_Princess_Map_Sprite.gif/revision/latest?cb=20160210044858'
            self.sprites['Nohr Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/d/de/FE14_Kanna_%28F%29_Dark_Blood_Map_Sprite.gif/revision/latest?cb=20160210044858'
            self.sprites['Hoshido Noble'] = 'https://static.wikia.nocookie.net/fireemblem/images/5/53/FE14_Kanna_%28F%29_White_Blood_Map_Sprite.gif/revision/latest?cb=20160210044858'

            self._set_classes_from_span(mother_span_two, 'heart', False)
            self._set_classes_from_span(father_span_two, 'heart', True)
            self._set_classes_from_span(buddy_span_two, 'buddy', False)
            self._set_classes_from_span(partner_span_two, 'partner', False)

        return None
    

    # ✨set child heart seals or all character buddy/partners
    def _set_classes_from_span(self, span, class_type, is_father):
        """
        takes in the <span>/whatever element before classes table element
        for each table in the classes element, gets the <td>s and calls _set_classes_from_tds
        """

        h_element = span.find_parent()
        classes_element = h_element.find_next_sibling()

        if classes_element.name == 'table':
            # get all the classes <td> elements
            classes = classes_element.find_all('td')
            self._set_classes_from_tds(classes, class_type, is_father)
        else:
            table_divs = classes_element.find_all('div', class_='wds-tab__content')
            tables = [div.find('table') for div in table_divs]
            for table in tables:
                # get all the classes <td> elements
                classes = table.find_all('td')
                self._set_classes_from_tds(classes, class_type, is_father)

        return None

    # ✨helper function for _set_classes_from_span to set child heart seals or all character buddy/partners
    def _set_classes_from_tds(self, classes, class_type, is_father):
        """
        takes in classes, an array of class <td> elements...
        and sets class names/sprites for either heart_sets, buddy_sets, or partner_sets
        class_type is a string, either 'heart', 'buddy', or 'partner'
        """

        # map class_type string to the correct dict attribute
        sets_map = {
            "heart": self.heart_sets,
            "buddy": self.buddy_sets,
            "partner": self.partner_sets
        }

        # pick the right dict for this run
        class_sets = sets_map[class_type]

        i = 0
        while i < len(classes):
            # Corrin cases
            if classes[i].find_all('a')[1].text.strip() == 'Corrin (F)' and class_type == 'heart':
                class_sets['Corrin'] = ['Nohr Princess', 'Nohr Noble', 'Hoshido Noble']
                i += 4 
                continue
            elif classes[i].find_all('a')[1].text.strip() == 'Corrin (M)' and class_type == 'heart':
                class_sets['Corrin'] = ['Nohr Prince', 'Nohr Noble', 'Hoshido Noble']
                i += 4 
                continue


            char_name = classes[i].find_all('a')[1].text.strip()
            # append to fathers/mothers if this is a child's parent tds
            if class_type == 'heart' and is_father:
                self.fathers.append(char_name)
            elif class_type == 'heart':
                self.mothers.append(char_name)

            # check if sprites exist
            a_tags = classes[i+1].find_all('a')
            if not a_tags:
                i += 4
                continue
            if len(a_tags) == 1:
                base = classes[i+1].find('a').text.strip() if classes[i+1].find('a') else ''
                promoted_one = classes[i+2].find('a').text.strip() if classes[i+2].find('a') else ''
                promoted_two = classes[i+3].find('a').text.strip() if classes[i+3].find('a') else ''
            else:  # sprites exist
                base = classes[i+1].find_all('a')[1].text.strip()
                promoted_one = classes[i+2].find_all('a')[1].text.strip()
                promoted_two = classes[i+3].find_all('a')[1].text.strip()
                # save sprites
                self.sprites[base] = classes[i+1].find_all('a')[0].get('href')
                self.sprites[promoted_one] = classes[i+2].find_all('a')[0].get('href')
                self.sprites[promoted_two] = classes[i+3].find_all('a')[0].get('href')

            # set classes into the correct dict
            class_sets[char_name] = [base, promoted_one, promoted_two]

            # handle multiple characters that give the same class
            char_a_tags = classes[i].find_all('a')
            if len(char_a_tags) > 3:
                class_sets[char_a_tags[3].text.strip()] = [base, promoted_one, promoted_two]
            if len(char_a_tags) > 5:
                class_sets[char_a_tags[5].text.strip()] = [base, promoted_one, promoted_two]

            i += 4


    # helper function to set child heartSeal (parent) classes
    def _set_child_heart_classes(self):
        """
        get an array of <td> elements that represent mother/father classes
        pass those into _set_classes_from_tds to set child heart classes
        """

        # get the <dt> element before the father classes
        father_dt = self.wiki_soup.find('dt', string='Inheritance from Father')
        mother_dt = self.wiki_soup.find('dt', string='Inheritance from Mother')

        self._set_classes_from_span(father_dt, 'heart', True)
        self._set_classes_from_span(mother_dt, 'heart', False)

        return None
    

    # helper function for set_classes, sets base/heart classes and sprites
    # for children, also sets father and mothers
    def _set_base_heart(self):
        """
        set base classes and sprites by parsing wiki_soup
        """
        
        # get the <h> element before the base/heart classes table
        span = self.wiki_soup.find("span", id="Standard_Sets")
        h_element = span.find_parent() if span else None

        # case for Selena, Laslow, Odin
        if self.name in ('Selena', 'Laslow', 'Odin'):
            if self.name == 'Selena':
                span = self.wiki_soup.find("span", id="Standard_Sets_2")
                h_element = span.find_parent() if span else None
            else:
                span = self.wiki_soup.find("b", string="Standard Sets")
                h_element = span.find_parent() if span else None
        
        # find the Standard Sets table
        standard_sets_table = h_element.find_next_sibling('table')
        # get all the standard classes <td> elements
        standard_classes = standard_sets_table.find_all('td')

        # loop through all standard sets classes
        i = 0
        while (i < len(standard_classes)):
            if i < 3: # set base classes names
                for k in range(3):
                    a_tags = standard_classes[k+i].find_all('a')
                    if a_tags:
                        self.base_class.append(a_tags[1].text.strip())
            else: # set heart seal classes names
                heart_base = standard_classes[i].find_all('a')[1].text.strip()
                heart_promoted_one = standard_classes[i+1].find_all('a')[1].text.strip()
                heart_promoted_two = standard_classes[i+2].find_all('a')[1].text.strip()
                self.heart_sets[heart_base] = [heart_base, heart_promoted_one, heart_promoted_two]
                
            for k in range(3): # loop through and get sprites
                # get the <a> element with sprite href
                sprite = standard_classes[i].find('a', class_='mw-file-description image')
                if (sprite):
                    # save sprite class name and href
                    self.sprites[standard_classes[i].find_all('a')[1].text.strip()] = sprite.get('href')
                i += 1
        
        if self.is_child:
            self._set_child_heart_classes()

        return None
     
    # helper function for set_classes, sets buddy/partner classes and sprites
    def _set_buddy_partner(self):
        """
        set buddy and partner classes + sprites
        by parsing wiki_soup and passing array of <td> elements (classes)
        into helper functions
        """
        
        # get the buddy and partner spans before their respective tables
        buddy_span = self.wiki_soup.find("span", id="Friendship_Sets")
        if buddy_span is None:
            buddy_span = self.wiki_soup.find('b', string='Friendship Sets')

        partner_span = self.wiki_soup.find("span", id="Partner_Sets")
        if partner_span is None:
            partner_span = self.wiki_soup.find('b', string='Partner Sets')

        # marriage span is the same as partner span, just one character has different text
        marriage_span = self.wiki_soup.find("span", id="Marriage_Sets")


        if buddy_span:
            self._set_classes_from_span(buddy_span, 'buddy', False)
        if partner_span:
            self._set_classes_from_span(partner_span, 'partner', False)
        if marriage_span:
            self._set_classes_from_span(marriage_span, 'partner', False)
                    
        return None

    # helper function, removes birthright characters from base/heart/buddy/partner sets
    def _remove_birthright(self):
        """
        iterate through heart/partner/buddy sets and remove birthright character entries
        """
        for sets in [self.heart_sets, self.partner_sets, self.buddy_sets]:
            for char_name in list(sets.keys()):  # use list() so we can modify while iterating
                if char_name in self.BIRTHRIGHT_CHARACTERS:
                    del sets[char_name]
        return None
    
    # set base/heart/buddy/partner classes + sprites + father/mothers
    def set_classes(self):
        """
        set all base/heart/buddy/partner classes using helper functions
        also remove Birthright characters from these classes
        """
        # Corrin case
        if self.name == 'Corrin':
            self._set_corrin_classes()

        # Kana case
        elif self.name == 'Kana M' or self.name == 'Kana F':

            self._set_kana_classes()

        # default case
        else:
            self._set_base_heart()
            self._set_buddy_partner()

        # remove birthright characters from class sets
        self._remove_birthright()

        return None
    
    # set all variables
    def set_all(self):
        """
        call each previous main function and populate all variables
        """
        self.populate_statbox_info()
        self.set_personal_skill()
        self.set_growth_rates()
        self.set_max_stats()
        self.set_classes()

        # print("Name:", self.name)
        # print("Is Child:", self.is_child)

        # print("Fathers:", self.fathers)
        # print("Mothers:", self.mothers)
        # print("Starting Class:", self.starting_class)
        # print("Start Level:", self.start_level)
        # print("Base Stats:", self.base_stats)

        # print("Personal Skill:", self.personal_skill)
        # print("Growth Rates:", self.growth_rates)
        # print("Max Stats:", self.max_stats)

        # print("Base Class:", self.base_class)
        # print("Heart Sets:", self.heart_sets)
        # print("Partner Sets:", self.partner_sets)
        # print("Buddy Sets:", self.buddy_sets)

        # print("Sprites:", self.sprites)

########################################################


# fill in a 'data' with character info, save as json file

data = []
sprites = []
names = get_character_names()
base_folder = "new_sprites"
os.makedirs(base_folder, exist_ok=True)

for name in names:
    time.sleep(0.3)
    c = Character(name)
    c.set_all()

    data.append({
        'name': c.name,
        'gender': c.gender,
        'isChild': c.is_child,
        'fathers': c.fathers,
        'mothers': c.mothers,
        'startingClass': c.starting_class,
        'startLevel': c.start_level,
        'baseStats': c.base_stats,

        'personalSkill': c.personal_skill,
        'growthRates': c.growth_rates,
        'maxStats': c.max_stats,
        "baseClass": c.base_class,
        "heartSets": c.heart_sets,
        "partnerSets": c.partner_sets,
        "buddySets": c.buddy_sets,
        # "sprites": c.sprites
    })

    sprites.append({
        'name': c.name,
        'sprites': c.sprites
    })
    print(c.name + ' added')


with open("characters.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open("sprites.json", "w", encoding="utf-8") as f:
    json.dump(sprites, f, indent=2, ensure_ascii=False)

# start = time.time()
# end = time.time()
# print(f"Runtime: {end - start:.4f} seconds")


###### Save sprites for this character #####
# NOTE: this would go in the [for name in names:] loop,
# after c.set_all()
    # char_folder = os.path.join(base_folder, c.name)
    # os.makedirs(char_folder, exist_ok=True)

    # for class_name, href in c.sprites.items():
    #     # Sanitize class name for filenames
    #     safe_class_name = class_name.replace(" ", "_").replace("/", "_")
    #     # Get extension from URL or default to .webp
    #     ext = os.path.splitext(href)[1] or ".webp"
    #     filename = f"{c.name}-{safe_class_name}{ext}"
    #     filepath = os.path.join(char_folder, filename)

    #     try:
    #         response = requests.get(href)
    #         if response.status_code == 200:
    #             with open(filepath, "wb") as f:
    #                 f.write(response.content)
    #             print(f"Saved {filename}")
    #         else:
    #             print(f"Failed to download {href}")
    #     except Exception as e:
    #         print(f"Error downloading {href}: {e}")

    #     time.sleep(0.1)  # polite delay
    ################################################