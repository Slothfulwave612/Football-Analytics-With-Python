import pandas as pd
from tqdm import tqdm

import my_utils, corner_utils, defence_utils

# load competition data
comp_data = my_utils.get_competition("../data/competitions.json")

# competition and season id
comp_id = 7
season_id = 1

# matches dataframe
match_df = my_utils.get_matches(f"../data/matches/{comp_id}/{season_id}.json")

# team name and player name
team = "Nantes"

match_df = match_df.loc[
    (match_df["home_team_name"] == team) |
    (match_df["away_team_name"] == team)
].reset_index(drop=True)

teams = [
    "Nantes", "PSG", "Lens"
]

matches = set()

for team in teams:
    temp_df = match_df.loc[
        (match_df["home_team_name"] == team) |
        (match_df["away_team_name"] == team)
    ]

    temp_teams = set(list(temp_df["home_team_name"].unique()) + list(temp_df["away_team_name"].unique()))

    for temp_team in temp_teams:
        if temp_team == team:
            continue
        if len(temp_df.loc[temp_df["home_team_name"] == temp_team]) == 0:
            matches.add(f"{temp_team} v {team}")
        if len(temp_df.loc[temp_df["away_team_name"] == temp_team]) == 0:
            matches.add(f"{team} v {temp_team}")

for i in matches:
    print(i)