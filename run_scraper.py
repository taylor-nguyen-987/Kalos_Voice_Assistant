from autoscraper import AutoScraper
from bs4 import BeautifulSoup as bs
import json
import requests
import re

#CONSTANTS
IMAGE = "https://www.serebii.net/xy/pokemon/650.png"

class KalosScraper():

      def add_to_json(self, name, profile):

            """Adds Pokemon's information to JSON file"""

            with open ("pokemon.json") as json_file:
                  data = json.load(json_file)
                  temp = data["pokemons"]
                  #n = {"name": str(name)}
                  temp[name] = profile

            with open ("pokemon.json", "w") as f:
                  json.dump(data, f, indent=4)

      def scrape(self, part, url):

            """Scrapes data about Kalos Pokemon from serebii.net"""

            auto_scraper = AutoScraper()
            images = auto_scraper.build(url=url, wanted_list=[IMAGE])
            
            page = requests.get(url)
            soup = bs(page.content, "lxml")
            pokemon_table = (soup.find_all("table", class_="tab"))[1]
            pokemans = (pokemon_table.find_all("tr"))[2:] #Get all "tr" tags except the header
            
            pokemon_dict = {}
            size = len(pokemans[0].find_all("td"))
            for i, pokemon in enumerate(pokemans[::2]):
                  td_tags = pokemon.find_all("td")

                  if len(td_tags) <= size and len(td_tags) > 3:

                        #NAME
                        name = (re.sub('[^a-zA-Z]+', '', td_tags[3].text)).lower()
                        
                        #ABILITIES
                        abilities = td_tags[4]
                        abilities = abilities.find_all("a")
                        abilities = [ability.text for ability in abilities]
                        
                        #TYPINGS
                        a_tags = td_tags[5].find_all("a")
                        typings = [] #List of typings of the pokemon
                        for tags in a_tags:
                              type = (((tags['href']).replace("/pokedex-xy/", "")).replace(".shtml", "")).capitalize() 
                              #Isolated the Pokemon's typing from link
                              typings.append(type)

                        #STATS
                        hp = td_tags[6].text
                        attack = td_tags[7].text
                        defense = td_tags[8].text
                        sa = td_tags[9].text #special attack
                        sd = td_tags[10].text #special defense
                        speed = td_tags[11].text 
                        
                        #TRAINERS WHO TRAINED THIS POKEMON AND THE TRAINERS' LOCATIONS
                        t_location_tags = td_tags[12]
                        all_tags = t_location_tags.find_all("a")
                        t_locations = [] #Default to empty list
                        if all_tags is not None:
                              for tag in all_tags:
                                    trainer_name = ((tag.next_sibling.replace("-", "")).strip()).replace("\u00e9", "e")
                                    trainer_location = tag.text
                                    t_locations.append([trainer_name, trainer_location])
                        #[Trainer's Name, Trainer's Location]

                        #LOCATION OF THE POKEMON IN POKEMON X
                        locations_tags = td_tags[13]
                        locations = [] #Default to empty list
                        all_l_tags = locations_tags.find_all("a")
                        if all_l_tags is not None:
                              locations = [[f"{tag.text}{tag.next_sibling.strip()}"] for tag in all_l_tags]
                        if "Friend Safari" in locations_tags.text:
                              locations+=["Friend Safari"]
                        
                        try:
                              self.add_to_json(name, [f"{images[i]}", typings, [hp, attack, defense, sa, sd, speed], 
                              t_locations, locations, part])
                        except:
                              self.add_to_json(name, [None, typings, [hp, attack, defense, sa, sd, speed], 
                              t_locations, locations, part])
            return pokemon_dict


    
if __name__ == "__main__":

    scraper = KalosScraper()

    links = {"Central Kalos": "https://www.serebii.net/xy/centralpokedex.shtml",
               "Coastal Kalos": "https://www.serebii.net/xy/coastalpokedex.shtml", 
                  "Mountain Kalos": "https://www.serebii.net/xy/mountainpokedex.shtml" }
    for key in links.keys():
        #Input: Part of Kalos, URL of the part of Kalos
        scraper.scrape(key, links[key])