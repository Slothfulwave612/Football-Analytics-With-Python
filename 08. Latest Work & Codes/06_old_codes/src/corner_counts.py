"""
To count total number of corners faced by an opponents.

Author: Anmol Durgapal / @slothfulwave612
"""

import pandas as pd
from tqdm import tqdm
import json 

import my_utils, corner_utils, defence_utils

# load competition data
comp_data = my_utils.get_competition("../data/competitions.json")

# competition and season id
comp_id = 1
season_id = 1

# matches dataframe
match_df = my_utils.get_matches(f"../data/matches/{comp_id}/{season_id}.json")

# list all teams
teams = match_df["home_team_name"].unique()

# shot-dict
corner_dict = dict()

for team in tqdm(teams, desc="Counting Shots", total=len(teams)):
    # shot count
    corner_count = 0

    # fetch match ids
    match_ids = match_df.loc[
        (match_df["home_team_name"] == team) |
        (match_df["away_team_name"] == team), "match_id"
    ].values

    for match_id in match_ids:
        # make event dataframe for one match
        event_df = my_utils.make_event_df(match_id)

        # make a new column - is_corner
        event_df["is_corner"] = event_df["qualifiers"].apply(
            lambda x: corner_utils.is_corner_(x)
        )

        corner_count += len(event_df.loc[
            (event_df["is_corner"] == True) &
            (event_df["team_name"] != team)
        ])
    
    corner_dict[team] = corner_count

with open("../_data_/corner_counts.json", "w") as outfile: 
    json.dump(corner_dict, outfile)

print(corner_dict)