import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from . import Arrows, my_utils, Pitch, defence_utils
  
# ## path to the data file
# path_event = "data/La_Liga/2020_21/03_barca_v_sevilla/events.json"
# path_player = "data/La_Liga/2020_21/03_barca_v_sevilla/players.json"
# path_rest = "data/La_Liga/2020_21/03_barca_v_sevilla/rest.json"

# ## load data
# json_event, json_player, json_rest = my_utils.load_data(path_event, path_player, path_rest)

# # ## player_name 
# player_name = "Sergio Busquets"

# # ## player id
# player_id = int(json_player[player_name])

# ## make event dataframe
# event_df = my_utils.make_event_df(json_event)

## --------------- All Defensive Activity ---------------

# df = event_df.loc[
#     (
#         (event_df["type_displayName"] == "Aerial") |
#         (event_df["type_displayName"] == "Tackle") |
#         (event_df["type_displayName"] == "Challenge") |
#         (event_df["type_displayName"] == "Clearance") |
#         (event_df["type_displayName"] == "Interception") |
#         (event_df["type_displayName"] == "BlockedPass") |
#         (event_df["type_displayName"] == "Foul")   
#     ) & 
#     (event_df["playerId"] == player_id) &
#     (event_df["outcomeType_displayName"] == "Unsuccessful")
# ]

# defence = defence_utils.Defence(
#     scatter_size=150, succ_color="#EFAA42", unsucc_color="#9F9F9F"
# )
# fig, ax = defence.plot_defensive(df, def_type="all_def_activity")
# plt.show()


## --------------- PPDA Charts ---------------
defence = defence_utils.Defence(
    line_color="#121212", pitch_color="#E8EDE7", orientation="horizontal",
    plot_arrow=True, sxy=(12,8)
)

## colormap
# cmap = [
#     "#222222", "#3A3A3A", "#515151", "#696969",   
#     "#808080", "#AF6D70", "#BC5E63", "#C94F56",
#     "#B3454B", "#873135"
# ]

cmap = [
    "#435568", "#556576", "#677584", "#798592", "#8B95A0",
    "#949DA7", "#9DA5AE", "#AFB5BC", "#C1C5CA", "#D2D4D8",
    "#D4C6CA", "#D5B8BC", "#D7A4A8", "#D9878B", "#DA7E82",
    "#DB7478", "#DC6065", "#DE4D52", "#DF393E"
]

fig, ax = defence.make_ppda_charts(
    competition_id=1,
    season_id=1,
    nrows=5,
    ncols=4,
    figsize=(20,16),
    team_name_color="#121212",
    cmap=cmap
)

# fig = my_utils.add_image(
#     "logos/la_liga_white.png", fig, 0.03, 0.98, 0.1, 0.1
# ) 7:30

## plot figure title
my_utils.plot_text_fig(
    fig, "#E8EDE7", x=0.03, y=1.0,
    s=f"Proportion of Defensive Actions to Opposition Passes | La Liga 2020-21", fontsize=27, 
    color="#121212", fontfamily="Liberation Serif", fontweight="bold", ha="left", va="center"
)

my_utils.plot_text_fig(
    fig, "#E8EDE7", x=0.94, y=0.02,
    s=f"visualization created by @slothfulwave612 | inspired by @statsbomb", fontsize=17, 
    color="#121212", fontfamily="Liberation Serif", fontstyle="italic", ha="right", va="center"
)

l1 = mpl.patches.FancyArrow(
    0.37, 0.02, 0.2, 0, transform=fig.transFigure, 
    figure=fig, ec="#121212", fc="#121212", width=0.0015, alpha=0.95
)
fig.lines.extend([l1])


fig.savefig(
    "plots/test_plots/ppda_test.jpg", bbox_inches="tight", dpi=500,
    facecolor=fig.get_facecolor()
)