"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module for making pass maps.
"""

## required packages/modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.pyplot import rcParams
import json
from tqdm import tqdm
from highlight_text import fig_text

from . import my_utils, pass_utils

rcParams["font.family"] = "serif"

# ## pandas option
# pd.set_option("display.max_rows", None)
# # pd.set_option("display.max_columns", None)

# comp_data = my_utils.get_competition("data/competitions.json")

# ## competition and season id
# comp_id = 2
# season_id = 1

# ## matches dataframe
# match_df = my_utils.get_matches(f"data/matches/{comp_id}/{season_id}.json")

# ## team and player name
# team = "Man Utd"
# player_name = "Bruno Fernandes"

# ## team match ids
# match_ids = match_df.loc[
#     (match_df["home_team_name"] == team) | 
#     (match_df["away_team_name"] == team), "match_id"
# ].values

# ## empty dataframes
# key_pass_df = pd.DataFrame()
# assist_df = pd.DataFrame()

# # traverse the match-ids
# for match_id in tqdm(match_ids, total=len(match_ids)):
#     ## read the lineups
#     lineup_json = json.load(open(f"data/lineups/{match_id}.json", encoding="utf-8"))

#     ## check if player is present in the match-lineup or not
#     if player_name in lineup_json.values():

#         ## make event dataframe for a particular match id
#         temp_event = my_utils.make_event_df(match_id)

#         ## required dataframe
#         pass_df = temp_event.loc[
#             (temp_event["type_displayName"] == "Pass") &
#             (temp_event["player_name"] == player_name)
#         ].copy()

#         ## make a new columns
#         pass_df["what_pass"] = pass_df["qualifiers"].apply(lambda x: my_utils.key_assist(x))

#         ## temp assist dataframe
#         temp_assist = pass_df.loc[
#             pass_df["what_pass"] == "Assist"
#         ].copy()

#         ## temp keypass dataframe
#         temp_key = pass_df.loc[
#             pass_df["what_pass"] == "Key Pass"
#         ].copy()

#         ## concat key-pass
#         key_pass_df = pd.concat(
#             [key_pass_df, temp_key]
#         )

#         ## concat assist
#         assist_df = pd.concat(
#             [assist_df, temp_assist]
#         )

# ## reset the index
# assist_df = assist_df.reset_index(drop=True)
# key_pass_df = key_pass_df.reset_index(drop=True)

assist_df = pd.read_pickle("assist.pkl")
key_pass_df = pd.read_pickle("key.pkl")
## pass object

pass_obj_2 = pass_utils.Pass(
    line_color="#B0B0B0", pitch_color="#222222", orientation="horizontal",
    arrow_type="simple_arrows", color="#D5432B", headlength=10, headwidth=10,
    alpha=0.8
)
## plot keypasses
fig, ax = pass_obj_2.plot_passes(
    key_pass_df, pass_type="all_passes"
)

# pass object
pass_obj = pass_utils.Pass(
    line_color="#B0B0B0", pitch_color="#222222", orientation="horizontal",
    arrow_type="simple_arrows", color="#efaa42", headlength=10, headwidth=10,
    alpha=1
)
## plot assist
fig, ax = pass_obj.plot_passes(
    assist_df, pass_type="all_passes", figax=(fig, ax)
)

## add image
fig = my_utils.add_image(
    "logos/man_utd.png", fig, 0.126, 0.795, 0.07, 0.07
) 

text_color = "#F2F2F2"

## add title
fig_text(
    x=0.19, y=0.83, s="Bruno Fernandes - <Assist> and <Key Pass>", size=28,
    color=text_color,  highlight_colors=["#F0B356", "#DA5844"], fig=fig
)    

## add subtitle
fig_text(
    x=0.19, y=0.805, s="Premier League | Season 2020-21", size=23,
    color=text_color, fig=fig
)    

## Armband
fig_text(
    x=0.895, y=0.8175, s="Armband", size=25.5,
    color=text_color, fig=fig, ha="right"
)    

## credits
fig_text(
    x=0.895, y=0.15, s="data: Opta via WhoScored | graphic: @slothfulwave612",
    size=10, color=text_color, fig=fig, ha="right", fontstyle="italic"
)   

ax.set(xlim=(-0.5,104.5), ylim=(-4,76))

fig.savefig("plots/Armband/sloth/02_bruno/08_pass_map.jpg", dpi=570, bbox_inches="tight")