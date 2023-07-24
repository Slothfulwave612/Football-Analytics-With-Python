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
shot_dict = dict()

for team in tqdm(teams, desc="Counting Shots", total=len(teams)):
    # shot count
    shot_count = 0

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

        # get indices for corners-event taken by the opponents
        indicies = event_df.loc[
            (event_df["team_name"] != team) &
            (event_df["is_corner"] == True)
        ].index

        for index in indicies:
            # fetch time in seconds
            curr_time = my_utils.cal_time(event_df, index)

            # go to next index
            temp_index = index + 1

            while temp_index < len(event_df) and my_utils.cal_time(event_df, temp_index) - curr_time <= 6:
                if event_df.loc[temp_index, "is_corner"] and event_df.loc[temp_index, "isShot"] is not True:
                    break

                elif event_df.loc[temp_index, "isShot"] is True:
                    shot_count += 1
                    break

                temp_index += 1
    
    shot_dict[team] = shot_count

# with open("../_data_/shot_counts.json", "w") as outfile: 
#     json.dump(shot_dict, outfile)

print(shot_dict)


# under 10 seconds
{
    'Wolves': 52, 'Leeds': 69, 'Man City': 28, 'West Ham': 41, 
    'Sheff Utd': 85, 'Tottenham': 53, 'Man Utd': 50, 'Brighton': 44, 
    'Newcastle': 80, 'Everton': 76, 'Southampton': 46, 'Leicester': 69, 
    'Fulham': 65, 'Arsenal': 55, 'Liverpool': 35, 'West Brom': 76, 
    'Chelsea': 45, 'Burnley': 76, 'Crystal Palace': 75, 'Aston Villa': 48
}

# under 6 seconds
{
    'Wolves': 46, 'Leeds': 64, 'Man City': 25, 'West Ham': 38, 
    'Sheff Utd': 79, 'Tottenham': 48, 'Man Utd': 44, 'Brighton': 33, 
    'Newcastle': 75, 'Everton': 69, 'Southampton': 42, 'Leicester': 61, 
    'Fulham': 60, 'Arsenal': 48, 'Liverpool': 34, 'West Brom': 71, 
    'Chelsea': 36, 'Burnley': 63, 'Crystal Palace': 65, 'Aston Villa': 40
}