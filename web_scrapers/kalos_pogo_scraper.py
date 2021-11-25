from autoscraper import AutoScraper
from bs4 import BeautifulSoup as bs
import requests
import re

#CONSTANTS
UNWANTED1 = "Not Currently Available"
UNWANTED2 = "\nNot currently availableStats calculated from main game"
UNWANTED3 = "Only available in France"
FIRST = "Chespin"
IMAGE = "/pokemongo/pokemon/650.png"

HP = "HP"
ATTACK = "Attack"
DEFENSE = "Defense"
MAX_CP = "Max CP"

class KalosGoScraper():

      """Scrapes data about Kalos Pokemon from POKEMON GO"""

      links = {"Kalos": "https://serebii.net/pokemongo/gen6pokemon.shtml"}
    
      def scrape(self):
            scraper = AutoScraper()
            url = self.links["Kalos"]
            pokemon_dict = {}

            #POKEMON NAMES
            pre_names = scraper.build(url=url, wanted_list=[FIRST])
            names = []
            for name in pre_names:
                  if UNWANTED1 in name:
                        names.append(name.replace(UNWANTED1, ""))
                  elif UNWANTED2 in name:
                        names.append(name.replace(UNWANTED2, ""))
                  elif UNWANTED3 in name:
                        names.append(name.replace(UNWANTED3, ""))
                  else:
                        names.append(name)
            #POKEMON IMAGES
            images = scraper.build(url=url, wanted_list=[IMAGE])

            #POKEMON TYPINGS AND STATS
            page = requests.get(url)
            soup = bs(page.content, "lxml")
            pokemon_table = (soup.find_all("table", class_="tab"))[1]
            pokemans = (pokemon_table.find_all("tr"))[1:]
            all_typings = []
            all_stats = []
            for pokemon in pokemans:
                  if HP in pokemon.text and ATTACK in pokemon.text and DEFENSE in pokemon.text and MAX_CP in pokemon.text: #Filter duplicate tables
                        #TYPINGS
                        information = pokemon.find_all("td")
                        a_tags = information[4].find_all('a', href=True)
                        typings = [] #List of typings of the pokemon
                        for tags in a_tags:
                              type = (((tags['href']).replace("/pokedex-sm/", "")).replace(".shtml", "")).capitalize() 
                              #Isolated the Pokemon's typing from link
                              typings.append(type)
                        all_typings.append(typings)

                        #STATS
                        table_stats = (pokemon.find_all("table"))[1] #2nd table contains the Pokemon's stats
                        ind_stats = table_stats.find_all("tr")
                        final_stats = []
                        for stat in ind_stats:
                              if not (stat.text.strip()).isalpha():
                                    string = (stat.text).replace(" ", "")
                                    temp = re.compile("([a-zA-Z]+)([0-9]+)")
                                    res = temp.match(string).groups() #in Tuples
                                    final_stats.append(res)
                        all_stats.append(final_stats)

            #POKEMON DICT
            for i, name in enumerate(names):
                  pokemon_dict[name] = [f"https://serebii.net{images[i]}", all_typings[i], all_stats[i]]
            print(pokemon_dict)