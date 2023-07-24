import pandas as pd
import matplotlib.pyplot as plt

from . import Arrows, my_utils, Pitch, defence_utils, pass_utils

## path to the data file
path_event = "data/La_Liga/2020_21/03_barca_v_sevilla/events.json"
path_player = "data/La_Liga/2020_21/03_barca_v_sevilla/players.json"
path_rest = "data/La_Liga/2020_21/03_barca_v_sevilla/rest.json"

## load data
json_event, json_player, json_rest = my_utils.load_data(path_event, path_player, path_rest)

## make event dataframe
event_df = my_utils.make_event_df(json_event)

## ---------------------- PPDA Charts ----------------------

## defensive dataframe
# def_df = event_df.loc[
#     (
#         (event_df["type_displayName"] == "Interception") |
#         (event_df["type_displayName"] == "Tackle") |
#         (event_df["type_displayName"] == "Aerial") |
#         (event_df["type_displayName"] == "Challenge") |
#         (event_df["type_displayName"] == "Foul") |
#         (event_df["type_displayName"] == "Pass") 
#     )
# ]

## cmap 
# cmap = ["#8A050C", "#C22A31", "#DE3C44", "#EC454D", "#EC4C53", "#DF4950", "#C44349", "#8E383C", "#582D2F", "#222222"]
# cmap = ["#8A050C", "#A62128", "#C23D44", "#DE5960", "#94393D", "#6F292C", "#5C2123", "#4C1E20", "#222222"]
# cmap = ["#DE5960", "#AB474C", "#923E42", "#85393D", "#783437", "#742F32", "#66292B", "#5C282A", "#492627", "#222222"]
# cmap = ["#873135", "#B3454B", "#C94F56", "#BC5E63", "#AF6D70", "#808080", "#696969", "#515151", "#3A3A3A", "#222222"]

# fig, ax = defence_utils.ppda_charts(
#     def_df, cmap=cmap, line_color="#121212"
# )

## ---------------------- PPDA Charts ----------------------


## ---------------------- Progressive passes ----------------------

## all the passes
# df = event_df.loc[
#     (event_df["type_displayName"] == "Pass") &
#     (event_df["playerId"] == 44721) &
#     (event_df["outcomeType_displayName"] == "Successful")
# ].copy()

## init object of Pass class
# pass_obj = pass_utils.Pass(
#     arrow_type="cirtri", radius=0.8, circle_fc="#EFAA42", circle_alpha=0.8,
#     circle_ec="#EFAA42", tri_fc="#EFAA42", tri_alpha=0.3
# )
# fig, ax = pass_obj.make_progressive_map(df, save_path="busi.jpg")
# plt.show()

## ---------------------- Progressive passes ----------------------


## ---------------------- Deep Progression ----------------------

pass_df = pd.DataFrame()

df = event_df.loc[
    (event_df["type_displayName"] == "Pass") &
    (event_df["playerId"] == 44721)
]

for _, data in df.iterrows():
    ## fetch all the qualifiers
    qualifiers = data["qualifiers"]

    ## init a variable
    go_further = 1

    ## include only OPEN PLAY passes
    for val in qualifiers:
        try:
            display_name = val["type"]["displayName"]
            if display_name in ["CornerTaken", "FreeKickTaken", "IndirectFreeKickTaken"]:
                go_further = 0
                break
        except Exception:
            pass
    
    if go_further == 1:
        pass_df = pass_df.append(data)
    
pass_obj = pass_utils.Pass(
    arrow_type="cirtri", radius=0.8, circle_fc="#EFAA42", circle_alpha=0.8,
    circle_ec="#EFAA42", tri_fc="#EFAA42", tri_alpha=0.3
)
fig, ax = pass_obj.plot_passes(
    df, pass_type="deep_completion", save_path="busi_deep.jpg"
)

## ---------------------- Deep Progression ----------------------