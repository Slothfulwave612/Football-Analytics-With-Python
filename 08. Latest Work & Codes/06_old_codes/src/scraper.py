"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module for scrapping data from whoscored.
"""
import os
from selenium import webdriver
from tqdm.auto import tqdm
import numpy as np
import pandas as pd
import json

class whoScored:
    """
    class for scraping the data.
    """

    def __init__(self, who_links, comp_name, country_name, gender, season, stage=None):
        """
        Function to initialize the object of the class.

        Args:
            link (list): list of links to be scrapped.
            comp_name (str): competition name.
            country_name (str): country name.
            gender (str): gender type.
            season (str): season name.
            stage (str, optional): stage of the competition. Defaults to None.
        """        
        self.who_links = who_links
        # self.under_links = under_links
        self.comp_name = comp_name
        self.country_name = country_name
        self.gender = gender
        self.season = season
        self.stage = stage
    
    def start_scraping(self):
        """
        Function to scrape the data from the link provided.
        """        
        # check for directories
        self.__check_for_dirs()

        # check for the counter file
        counter = self.__counter_file()

        # get links
        who_link_file = self.__get_who_links()
        # under_link_file = self.__get_under_links()

        # get competitions
        comp = self.__get_competition()

        # fetch competition id, season id
        comp_id = counter["competition_id"][self.comp_name]
        season_id = counter["season_id"][self.season]

        # check for competition
        if len(comp) == 0:
            # create a teamp-dict
            temp_dict = {
                "competition_id": comp_id, "season_id": season_id, "country_name": self.country_name,
                "competition_name": self.comp_name, "competition_gender": self.gender,
                "season_name": self.season
            }

            # append to comp list
            comp.append(temp_dict)
        
        else:
            # create a competition dataframe
            comp_df = pd.DataFrame(comp)

            # check if competition and season is present or not
            length_df = len(comp_df.loc[
                (comp_df["competition_id"] == comp_id) &
                (comp_df["season_id"] == season_id)
            ])

            # whether competition or season not present
            if length_df == 0:
                # create a temp-dict
                temp_dict = {
                    "competition_id": comp_id, "season_id": season_id, "country_name": self.country_name,
                    "competition_name": self.comp_name, "competition_gender": self.gender,
                    "season_name": self.season
                }

                # append to comp list
                comp.append(temp_dict)
            
        # check for match file in match directory
        if os.path.isfile(f"../data/matches/{comp_id}/{season_id}.json") == True:
            match_data = json.load(open(f"../data/matches/{comp_id}/{season_id}.json", encoding="utf-8"))
        else:
            match_data = []

        # traverse the link-list
        for who_link in tqdm(self.who_links, desc="Scrapping Matches", total=len(self.who_links)):
            
            # if already present
            if who_link_file.get(who_link) == True:
                continue

            # scrape the event-data
            events, players, rest = self.scrape(who_link)

            # append the link in links dict
            who_link_file[who_link] = True

            # scrape the xg-data
            # if under_link != "none":
            #     content = self.scrape(under_link, xg=True)
            #     under_link_file[under_link] = True
            # else:
            #     content = {
            #         "value": "none"
            #     }

            # check for match directory
            if os.path.isdir(f"../data/matches/{comp_id}") == False:
                os.mkdir(f"../data/matches/{comp_id}")

            # fetch match id from counter by incrementing the counter by 1
            counter["match_id"] = counter["match_id"] + 1
            match_id = counter["match_id"]

            # penalty kick score
            if rest["pkScore"] == '':
                pk_home, pk_away = np.nan, np.nan
            else:
                pk_home = rest["pkScore"].split(" : ")[0]
                pk_away = rest["pkScore"].split(" : ")[1]

            # ADDING CHANGES
            if rest["htScore"] == '':
                rest["htScore"] = "0 : 0"
            
            if rest["ftScore"] == '':
                rest["ftScore"] = "0 : 0"

            if rest.get("referee") is None:
                referee = None
            else:
                referee = rest["referee"]["name"]

            # match info
            if self.stage == None:
                temp_match = {
                    "match_id": match_id, "match_date": rest["startDate"], 
                    "competition": {
                        "id": comp_id, "name": self.comp_name, "country_name": self.country_name
                    },
                    "season": {
                        "id": season_id, "name": self.season
                    },
                    "home_team": {
                        "id": rest["home"]["teamId"],
                        "name": rest["home"]["name"],
                        "manager_name": rest["home"]["managerName"]
                    },
                    "away_team": {
                        "id": rest["away"]["teamId"],
                        "name": rest["away"]["name"],
                        "manager_name": rest["away"]["managerName"]
                    },
                    "home_score_ht": rest["htScore"].split(" : ")[0],
                    "away_score_ht": rest["htScore"].split(" : ")[1],
                    "home_score_ft": rest["ftScore"].split(" : ")[0],
                    "away_score_ft": rest["ftScore"].split(" : ")[1],
                    "home_score_pk": pk_home, "away_score_pk": pk_away,
                    "venue_name": rest["venueName"],
                    "referee": referee
                }
            else:
                temp_match = {
                    "match_id": match_id, "match_date": rest["startDate"], 
                    "competition": {
                        "id": comp_id, "name": self.comp_name, "country_name": self.country_name
                    },
                    "stage": self.stage,
                    "season": {
                        "id": season_id, "name": self.season
                    },
                    "home_team": {
                        "id": rest["home"]["teamId"],
                        "name": rest["home"]["name"],
                        "manager_name": rest["home"]["managerName"]
                    },
                    "away_team": {
                        "id": rest["away"]["teamId"],
                        "name": rest["away"]["name"],
                        "manager_name": rest["away"]["managerName"]
                    },
                    "home_score_ht": rest["htScore"].split(" : ")[0],
                    "away_score_ht": rest["htScore"].split(" : ")[1],
                    "home_score_ft": rest["ftScore"].split(" : ")[0],
                    "away_score_ft": rest["ftScore"].split(" : ")[1],
                    "home_score_pk": pk_home, "away_score_pk": pk_away,
                    "venue_name": rest["venueName"],
                    "referee": rest["referee"]["name"]
                }

            # append temp_match dict to match_data list            
            match_data.append(temp_match)
            
            # make files
            event_file = open(f"../data/events/{match_id}.json", "w")
            # xg_file = open(f"../data/xg_events/{match_id}.json", "w")
            player_file = open(f"../data/lineups/{match_id}.json", "w")
            rest_file = open(f"../data/rest/{match_id}.json", "w")

            # save scrapped files ---> json format
            json.dump(events, event_file, indent=2)
            # json.dump(content, xg_file, indent=2)
            json.dump(players, player_file, indent=2)
            json.dump(rest, rest_file, indent=2)

            # close the files
            event_file.close()
            # xg_file.close()
            player_file.close()
            rest_file.close()
        
        # make files
        comp_file = open("../data/competitions.json", "w")
        match_file = open(f"../data/matches/{comp_id}/{season_id}.json", "w")
        counter_file = open("../data/counter.json", "w")
        link_file_1 = open("../data/who_links.json", "w")
        # link_file_2 = open("../data/under_links.json", "w")

        # save the rest
        json.dump(comp, comp_file, indent=2)
        json.dump(match_data, match_file, indent=2)
        json.dump(counter, counter_file, indent=2)
        json.dump(who_link_file, link_file_1, indent=2)
        # json.dump(under_link_file, link_file_2, indent=2)

        # close the files
        comp_file.close()
        match_file.close()
        counter_file.close()
        link_file_1.close()
        # link_file_2.close()

    def __check_for_dirs(self):
        """
        Function to check for directories.
        """
        if os.path.isdir("../data") == False:
            os.mkdir("../data")
        
        if os.path.isdir("../data/events") == False:
            os.mkdir("../data/events")
        
        # if os.path.isdir("../data/xg_events") == False:
        #     os.mkdir("../data/xg_events")
            
        if os.path.isdir("../data/lineups") == False:
            os.mkdir("../data/lineups")
        
        if os.path.isdir("../data/rest") == False:
            os.mkdir("../data/rest")
        
        if os.path.isdir("../data/matches") == False:
            os.mkdir("../data/matches")
        
    def __counter_file(self):
        """
        Function to build/fetch up/from the counter file.

        Returns:
            dict: containing counter file info.
        """        
        # check whether the file is present or not
        if os.path.isfile("../data/counter.json") == True:
            # load the counter file
            counter = json.load(open("../data/counter.json", encoding="utf-8"))

            # check for match_id
            if counter.get("match_id") == False or counter.get("competition_id") == False or counter.get("season_id") == False:
                raise ValueError("Some key is not present!!! Please check!!!")
            
            # if competition is not present 
            if counter["competition_id"].get(self.comp_name) == None:
                # fetch the max comp-id
                comp_id = max(counter["competition_id"].values())

                # append the info in the dict
                counter["competition_id"][self.comp_name] = comp_id + 1
            
            # if season is not present
            if counter["season_id"].get(self.season) == None:
                # fetch the max season id
                season_id = max(counter["season_id"].values())

                # append the info in the dict
                counter["season_id"][self.season] = season_id + 1

        else:
            # if not present create a counter dict(empty)
            counter = {}

            # assign match-id to 0
            counter["match_id"] = 0

            # assign competition-id
            counter["competition_id"] = {self.comp_name: 1}

            # assign season-id
            counter["season_id"] = {self.season: 1}
        
        return counter

    def __get_who_links(self):
        """
        Function to build or grab the links(already scraped) for whoscored.

        Returns:
            dict: containing links.
        """        
        # check for file
        if os.path.isfile("../data/who_links.json") == False:
            return {}

        # load links
        links = json.load(open("../data/who_links.json", encoding="utf-8"))
        
        return links

    def __get_under_links(self):
        """
        Function to build or grab the links(already scraped) for understats.

        Returns:
            dict: containing links.
        """        
        # check for file
        if os.path.isfile("../data/under_links.json") == False:
            return {}

        # load links
        links = json.load(open("../data/under_links.json", encoding="utf-8"))
        
        return links

    def __get_competition(self):
        """
        Function to build/grab competition file.

        Returns:
            list: of competition value.
        """        
        # check for file
        if os.path.isfile("../data/competitions.json") == False:
            return []
        
        # load competition file
        comp = json.load(open("../data/competitions.json", encoding="utf-8"))

        return comp

    
    def scrape(self, link, xg=False, path=None):
        """
        Function to scrape data from the website.

        Args:
            link (str): link for the webpage to be scrapped.
            xg (bool, optional): to scrape the xg data.
            path (str, optional): path where the data will be saved. Defaults to None.

        Returns:
            tuple: containing scraping info for event data, player data and rest data.
        """ 
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # ready the chrome-drivers
        driver = webdriver.Chrome("C:/Chrome_Drivers/chromedriver", options=options)

        # give the link
        driver.get(link)

        # get the match data
        if xg:
            content = driver.execute_script("return shotsData;")

            # close the driver
            driver.close()
            
            return content
        else:
            # fetch the script tag
            element = driver.find_element_by_xpath('//*[@id="layout-wrapper"]/script[1]')

            # fetch the code inside script tag
            script_content = element.get_attribute('innerHTML')

            # format the string
            script_ls = script_content.split(sep="  ")
            script_ls = list(filter(None, script_ls))
            script_ls = [name for name in script_ls if name.strip()]
            dictstring = script_ls[2][17:-2]

            # get final content
            content = json.loads(dictstring)

        # close the driver
        driver.close()

        # event data
        event_data = content["events"]

        # player name dict
        player_data = content["playerIdNameDictionary"]

        # del unnecessary data
        del content["events"]
        del content["playerIdNameDictionary"]

        if path:
            # open files
            event_file = open(path + "/" + "events.json", "w")
            player_file = open(path + "/" + "players.json", "w")
            rest_file = open(path + "/" + "rest.json", "w")

            # save the files
            json.dump(event_data, event_file, indent=2) 
            json.dump(player_data, player_file, indent=2)
            json.dump(content, rest_file, indent=2)
            
            # close all the files
            event_file.close()
            player_file.close()
            rest_file.close()
            
        return event_data, player_data, content