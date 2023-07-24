"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python file for testing the pass_flow module.
"""

import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

from . import my_utils, heatmap, Pitch

## path to the data file
path_event = "data/La_Liga/2020_21/01_barca_v_villarreal/events.json"
path_player = "data/La_Liga/2020_21/01_barca_v_villarreal/players.json"
path_rest = "data/La_Liga/2020_21/01_barca_v_villarreal/rest.json"

## load data
json_event, json_player, json_rest = my_utils.load_data(path_event, path_player, path_rest)

## fetch home team and away team ids
home_team_id = json_rest["home"]["teamId"]
away_team_id = json_rest["away"]["teamId"]

## make event dataframe
event_df = my_utils.make_event_df(json_event)

# ## player_name 
# player_name = "Sergi Roberto"

# ## player id
# player_id = int(json_player[player_name])

## pass dataframe for Barcelona(here home team)
# pass_df = event_df.loc[
#     (event_df["type_displayName"] == "Pass") &
#     (event_df["playerId"] == player_id) 
# ].reset_index(drop=True)

## half
half = event_df.loc[
    (event_df["type_displayName"] == "Pass") & 
    (event_df["teamId"] == home_team_id)
]

# # cmap list
cmap = ["#2A2A2A", "#3C2A2A", "#693A39", "#844140", "#9E4746", "#A84948", "#D25352"]
# cmap = ["#222222", "#372429", "#4B2530", "#5F2737", "#69283B", "#6E283D", "#73283E"]

## create heatmap
# pass_flow = heatmap.Heatmap(
#     pass_flow=False, line_color="#949C94", pitch_color="#2A2A2A", 
#     show=True, arrow_length=4, arrow_color="#F2F2F2", cmap=cmap, plot=True
# )
# pass_flow.create_heatmap(
#     half, bins=(5,5), zorder=2
# )

# , filename="plots/Barcelona/La_Liga/2020_21/01_barca_v_villarreal/half_2p.jpg"

ht = heatmap.Heatmap(
    pass_flow=False, line_color="#9C9C9C", pitch_color="#222222", 
    show=True, arrow_length=4, arrow_color="#F2F2F2", cmap=cmap, plot=True, alpha=0.85
)
fig, ax = ht.create_aligned_heatmap(half)