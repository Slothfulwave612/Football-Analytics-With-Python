# required packages/modules
import pandas as pd
from tqdm import tqdm

import my_utils, corner_utils, defence_utils

# load competition data
comp_data = my_utils.get_competition("../data/competitions.json")

# competition and season id
comp_id = 1
season_id = 1

# matches dataframe
match_df = my_utils.get_matches(f"../data/matches/{comp_id}/{season_id}.json")

# team name and player name
team = "Barcelona"

# team match ids
match_ids = match_df.loc[
    (match_df["home_team_name"] == team) |
    (match_df["away_team_name"] == team), "match_id"
].values

event_df = pd.DataFrame()

for match_id in tqdm(match_ids, total=len(match_ids)):
    event = my_utils.make_event_df(match_id)

    event_df = pd.concat([event_df, event])
    break

print(event_df.loc[50, "qualifiers"])

# event_df = event_df.reset_index(drop=True)
# event_df.to_pickle("../_data_/barca/all_shots.pkl")

# for match_id in tqdm(match_ids, total=len(match_ids)):
#     event = my_utils.make_event_df(match_id)

#     event = event.loc[
#         (event["team_name"] == team) &
#         (event["type_displayName"].isin(
#             [
#                 "Interception", "Challenge",
#                 "BlockedPass", "Tackle"
#             ]
#         ))
#     ]

#     event_df = pd.concat([event_df, event])

# event_df = event_df.reset_index(drop=True)
# event_df.to_pickle("../_data_/barca/defensive_info.pkl")

# defence = defence_utils.Defence(
#     line_color="#121212", pitch_color="#E8EDE7", orientation="horizontal",
#     plot_arrow=True, sxy=(12,8)
# )

# ppda_values, teams = defence.get_ppda_values(1, 1)

# print(ppda_values)
# print(teams)

# event_df = pd.DataFrame()

# for match_id in tqdm(match_ids, total=len(match_ids)):
#     event = my_utils.make_event_df(match_id)

#     event = event.loc[
#         (event["team_name"] != team) &
#         (event["isTouch"] == True) &
#         (event["type_displayName"].isin(
#             ["Pass", "BallTouch", "Goal", "MissedShots", "ShotOnPost", "GoodSkill"]
#         ))
#     ]

#     event_df = pd.concat([event_df, event])

# event_df = event_df.reset_index(drop=True)
# print(event_df["type_displayName"].unique())

# event_df.to_pickle("../_data_/barca/opponent_data.pkl")

# player_info = {}

# for match_id in tqdm(match_ids, total=len(match_ids)):
#     event = my_utils.make_event_df(match_id)

#     event["is_free_kick"] = event["qualifiers"].apply(
#         lambda x: my_utils.is_free_kick(x)
#     )

#     event["is_corner"] = event["qualifiers"].apply(
#         lambda x: corner_utils.is_corner_(x)
#     )

#     indicies = event.loc[
#         (event["team_name"] != team) &
#         (
#             (event["is_free_kick"] == True) |
#             (event["is_corner"] == True)
#         )
#     ].index
    
#     for index in indicies:
#         curr_time = my_utils.cal_time(event, index)
#         temp_index = index + 1

#         while temp_index < len(event) and my_utils.cal_time(event, temp_index) - curr_time <= 10:
#             # print(event.loc[temp_index, "type_displayName"])
#             if event.loc[temp_index, "team_name"] != team:
#                 temp_index += 1

#             if (event.loc[temp_index, "is_corner"]) | (event.loc[temp_index, "is_free_kick"]):
#                 break

#             elif event.loc[temp_index, "type_displayName"] in ["Aerial"] and event.loc[temp_index, "team_name"] == team:
#                 succ, unsucc = 0, 0

#                 player_name = event.loc[temp_index, "player_name"]
#                 outcome = event.loc[temp_index, "outcomeType_displayName"]

#                 if player_info.get(player_name) is None:
#                     if outcome == "Successful":
#                         succ = 1
#                     elif outcome == "Unsuccessful":
#                         unsucc = 1
#                     player_info[player_name] = {
#                         "successful": succ, "unsuccessful": unsucc
#                     }
#                 else:
#                     if outcome == "Successful":
#                         succ = player_info[player_name]["successful"]
#                         player_info[player_name]["successful"] = succ + 1
#                     else:
#                         unsucc = player_info[player_name]["unsuccessful"]
#                         player_info[player_name]["unsuccessful"] = unsucc + 1

#             temp_index += 1 

# print(player_info)

# import pandas as pd
# from tqdm import tqdm

# import my_utils, corner_utils, defence_utils

# # load competition data
# comp_data = my_utils.get_competition("../data/competitions.json")

# # competition and season id
# comp_id = 10
# season_id = 1

# # matches dataframe
# match_df = my_utils.get_matches(f"../data/matches/{comp_id}/{season_id}.json")

# print(match_df[["home_team_name", "away_team_name", "match_id"]])
# print(match_df["home_team_name"].value_counts())
# print(match_df["away_team_name"].value_counts())