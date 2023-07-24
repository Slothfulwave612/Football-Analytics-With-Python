"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module for scraping given links.
"""

import scraper

who_links = [
    "https://1xbet.whoscored.com/Matches/1575792/Live/Italy-Serie-A-2021-2022-Fiorentina-Torino",
    "https://1xbet.whoscored.com/Matches/1575801/Live/Italy-Serie-A-2021-2022-Atalanta-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575812/Live/Italy-Serie-A-2021-2022-Genoa-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575824/Live/Italy-Serie-A-2021-2022-Fiorentina-Inter",
    "https://1xbet.whoscored.com/Matches/1575848/Live/Italy-Serie-A-2021-2022-Udinese-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575834/Live/Italy-Serie-A-2021-2022-Fiorentina-Napoli",
    "https://1xbet.whoscored.com/Matches/1575860/Live/Italy-Serie-A-2021-2022-Venezia-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575863/Live/Italy-Serie-A-2021-2022-Fiorentina-Cagliari",
    "https://1xbet.whoscored.com/Matches/1575874/Live/Italy-Serie-A-2021-2022-Lazio-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575883/Live/Italy-Serie-A-2021-2022-Fiorentina-Spezia",
    "https://1xbet.whoscored.com/Matches/1575893/Live/Italy-Serie-A-2021-2022-Juventus-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575903/Live/Italy-Serie-A-2021-2022-Fiorentina-AC-Milan",
    "https://1xbet.whoscored.com/Matches/1575912/Live/Italy-Serie-A-2021-2022-Empoli-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575923/Live/Italy-Serie-A-2021-2022-Fiorentina-Sampdoria",
    "https://1xbet.whoscored.com/Matches/1575931/Live/Italy-Serie-A-2021-2022-Bologna-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575941/Live/Italy-Serie-A-2021-2022-Fiorentina-Salernitana",
    "https://1xbet.whoscored.com/Matches/1575954/Live/Italy-Serie-A-2021-2022-Fiorentina-Sassuolo",
    "https://1xbet.whoscored.com/Matches/1575963/Live/Italy-Serie-A-2021-2022-Verona-Fiorentina",
    "https://1xbet.whoscored.com/Matches/1575998/Live/Italy-Serie-A-2021-2022-Torino-Fiorentina"
]

# if not present pass "none"
under_links = []

comp_name = "Serie A"                      
country_name = "Italy"
gender = "Male"
season = "2021/2022" 

# create object of whoScored class
# if len(under_links) == len(who_links) and (len(under_links) != 0 or len(who_links) != 0):
ws_scraper = scraper.whoScored(
    who_links,
    comp_name, 
    country_name, 
    gender, 
    season,
)

## scrape the links 
ws_scraper.start_scraping()
# else:
#     print("Bummer!!!")