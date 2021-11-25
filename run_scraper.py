from web_scrapers.kalos_scraper import KalosScraper

def run(scraper="kalos_scraper"):

    """Runs the scrapers in web_scrapers folder"""
    
    scraper = KalosScraper()
    scraper.scrape()
    
    
if __name__ == "__main__":
    run()

#import importlib

#mod = importlib.import_module(f"web_scrapers.{scraper}")
    #kclass = getattr(mod, "KalosScraper")
    #scraper = kclass()
    #scraper.scrape()