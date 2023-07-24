import pandas as pd
import matplotlib.pyplot as plt

from . import defence_utils, pass_utils, my_utils, heatmap, Pitch

## path to the data file
path_event_1 = "data/La_Liga/2020_21/01_barca_v_villarreal/events.json"
path_player_1 = "data/La_Liga/2020_21/01_barca_v_villarreal/players.json"
path_event_2 = "data/La_Liga/2020_21/02_celta_v_barca/events.json"
path_player_2 = "data/La_Liga/2020_21/02_celta_v_barca/players.json"
path_event_3 = "data/La_Liga/2020_21/03_barca_v_sevilla/events.json"
path_player_3 = "data/La_Liga/2020_21/03_barca_v_sevilla/players.json"

## load data
json_event_1, json_player_1 = my_utils.load_data(path_event_1, path_player_1)
json_event_2, json_player_2 = my_utils.load_data(path_event_2, path_player_2)
json_event_3, json_player_3 = my_utils.load_data(path_event_3, path_player_3)

## make event dataframe
event_df_1 = my_utils.make_event_df(json_event_1)
event_df_2 = my_utils.make_event_df(json_event_2)
event_df_3 = my_utils.make_event_df(json_event_3)

## player_name 
player_name = "Philippe Coutinho"

# ## player id
player_id = int(json_player_1[player_name])

event_df = pd.concat([event_df_1, event_df_2, event_df_3], axis=0).reset_index(drop=True)

## -------------- Touches --------------

## create touch dataframe
# touch_df = event_df.loc[
#     (event_df["isTouch"] == True) &
#     (event_df["playerId"] == player_id)
# ].copy()

# ## cmap
# cmap = ["#222222", "#2D2424", "#382626", "#432828", "#4D2929", "#632C2C", "#6E2E2E", "#843131", "#993434", "#A33535", "#AE3737", "#B93838", "#CE3B3B"]

# name = "plots/Barcelona/La_Liga/2020_21/03_barca_v_sevilla/coutinho/02_heatmap.jpg"

# ## init object of Pitch class
# fig, ax = plt.subplots(figsize=(12,8), facecolor="#222222")
# ax.set_facecolor("#222222")

# ## init object of heatmap class
# heat_obj = heatmap.Heatmap(
#     line_color="#ececec", pitch_color="#222222", 
#       cmap=cmap, show=False, interpolation="gaussian"
# )
# fig, ax = heat_obj.make_heatmap(
#     touch_df, heat_type="simple_heatmap", bins=(10,10), filename=name, image_path="logos/fcb.png",
#     orientation_array=[-0.04, 0.83, 0.4, 0.07], main_title=f"{player_name} - Touches",
#     sub_title="La Liga | Season 2020/2021", credit="created by @slothfulwave612", figax=(fig, ax),
#     main_size=19, sub_size=15, credit_size=8,
#     main_coord=(7,73), sub_coord=(7,70), credit_coord=(103.5,1), font="Gayathri"
# )

## -------------- Touches --------------


## -------------- Reception Zones --------------

## create a pass dataframe
# pass_df = event_df.loc[
#     (event_df["type_displayName"] == "Pass") & 
#     (event_df["playerId"] == player_id)
# ].copy()

# ## create an empty dataframe
# reception_df = pd.DataFrame()

# ## traverse through the index of pass_df
# for index in pass_df.index:
#     if event_df.loc[index-1, "type_displayName"] == "Pass":
#         reception_df = reception_df.append(event_df.loc[index])
    
# ## color map    
# cmap = ["#222222", "#2D2424", "#382626", "#432828", "#4D2929", "#632C2C", "#6E2E2E", "#843131", "#993434", "#A33535", "#AE3737", "#B93838", "#CE3B3B"]

# ## name of the plot
# name = "plots/Barcelona/La_Liga/2020_21/03_barca_v_sevilla/coutinho/04_recpt_heatmap.jpg"

# ## init object of Pitch class
# fig, ax = plt.subplots(figsize=(12,8), facecolor="#222222")
# ax.set_facecolor("#222222")

# ## init object of heatmap class
# heat_obj = heatmap.Heatmap(
#     line_color="#ececec", pitch_color="#222222", cmap=cmap, show=False, interpolation="gaussian"
# )
# fig, ax = heat_obj.make_heatmap(
#     reception_df, heat_type="simple_heatmap", bins=(10,10), filename=name, image_path="logos/fcb.png",
#     orientation_array=[-0.04, 0.83, 0.4, 0.07], main_title=f"{player_name} - Reception Zones",
#     sub_title="La Liga | Season 2020/2021", credit="created by @slothfulwave612", figax=(fig, ax),
#     main_size=19, sub_size=15, credit_size=8,
#     main_coord=(7,73), sub_coord=(7,70), credit_coord=(103.5,1), font="Gayathri"
# )

## -------------- Reception Zones --------------


## -------------- Passing Zones --------------

## create a pass dataframe
# df = event_df.loc[
#     (event_df["type_displayName"] == "Pass") & 
#     (event_df["playerId"] == player_id)
# ].copy()

# ## create an empty dataframe
# pass_df = pd.DataFrame()

# for _, data in df.iterrows():
#     ## fetch all the qualifiers
#     qualifiers = data["qualifiers"]

#     ## init a variable
#     go_further = 1

#     ## include only OPEN PLAY passes
#     for val in qualifiers:
#         try:
#             display_name = val["type"]["displayName"]
#             if display_name in ["CornerTaken", "FreeKickTaken", "IndirectFreeKickTaken"]:
#                 go_further = 0
#                 break
#         except Exception:
#             pass
    
#     if go_further == 1:
#         pass_df = pass_df.append(data)

# pass_df['x'] = pass_df['endX']
# pass_df['y'] = pass_df['endY']

# ## color map    
# cmap = ["#222222", "#2D2424", "#382626", "#432828", "#4D2929", "#632C2C", "#6E2E2E", "#843131", "#993434", "#A33535", "#AE3737", "#B93838", "#CE3B3B"]

# ## name of the plot
# name = "plots/Barcelona/La_Liga/2020_21/03_barca_v_sevilla/coutinho/06_passing_heatmap.jpg"

# ## init object of Pitch class
# fig, ax = plt.subplots(figsize=(12,8), facecolor="#222222")
# ax.set_facecolor("#222222")

# ## init object of heatmap class
# heat_obj = heatmap.Heatmap(
#     line_color="#ececec", pitch_color="#222222", cmap=cmap, show=False, interpolation="gaussian"
# )
# fig, ax = heat_obj.make_heatmap(
#     pass_df, heat_type="simple_heatmap", bins=(10,10), filename=name, image_path="logos/fcb.png",
#     orientation_array=[-0.04, 0.83, 0.4, 0.07], main_title=f"{player_name} - Passing Zones",
#     sub_title="La Liga | Season 2020/2021", credit="created by @slothfulwave612", figax=(fig, ax),
#     main_size=19, sub_size=15, credit_size=8,
#     main_coord=(7,73), sub_coord=(7,70), credit_coord=(103.5,1), font="Gayathri"
# )

## -------------- Passing Zones --------------

## -------------- All passes --------------

# create a pass dataframe
# df = event_df.loc[
#     (event_df["type_displayName"] == "Pass") & 
#     (event_df["playerId"] == player_id)
# ].copy()

# ## create an empty dataframe
# pass_df = pd.DataFrame()

# for _, data in df.iterrows():
#     ## fetch all the qualifiers
#     qualifiers = data["qualifiers"]

#     ## init a variable
#     go_further = 1

#     ## include only OPEN PLAY passes
#     for val in qualifiers:
#         try:
#             display_name = val["type"]["displayName"]
#             if display_name in ["CornerTaken", "FreeKickTaken", "IndirectFreeKickTaken"]:
#                 go_further = 0
#                 break
#         except Exception:
#             pass
    
#     if go_further == 1:
#         pass_df = pass_df.append(data)

# ## subplots
# fig, ax = plt.subplots(figsize=(12.5,8), facecolor="#222222")
# ax.set_facecolor("#222222")

# ## name of the plot
# name = "plots/Barcelona/La_Liga/2020_21/03_barca_v_sevilla/coutinho/07_all_passes.jpg"

# ## init object of Pass class
# pass_obj = pass_utils.Pass(
#     pitch_color="#222222", orientation="horizontal",
#     radius=0.8, circle_fc="#efaa42", circle_alpha=0.8,
#     circle_ec="#121212", circle_fc_uns="#222222", circle_alpha_uns=0.5,
#     circle_ec_uns="#9F9F9F", tri_fc_uns="#9F9F9F", tri_alpha_uns=0.5, 
#     tri_fc="#efaa42", tri_alpha=0.3)
# fig, ax = pass_obj.plot_passes(
#     pass_df, pass_type="all_passes",
#     save_path=name, image_path="logos/fcb.png",
#     orientation_array=[-0.02, 0.84, 0.4, 0.07], main_title=f"{player_name} - Pass Map",
#     sub_title="La Liga | Season 2020/2021", credit="created by @slothfulwave612", figax=(fig, ax),
#     main_size=19, sub_size=15, credit_size=8,
#     main_coord=(8,73), sub_coord=(8,70), credit_coord=(103.5,1), font="Gayathri"
# )

## -------------- All passes --------------

## -------------- Progressive Passes --------------

df = event_df.loc[
    (event_df["type_displayName"] == "Pass") & 
    (event_df["playerId"] == player_id)
].copy()

## create an empty dataframe
pass_df = pd.DataFrame()
key_df = pd.DataFrame()

for _, data in df.iterrows():
    if data["outcomeType_displayName"] == "Unsuccessful":
        continue

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

## flip columns for x,y and endX and endY for vertical pitch-map
temp = pass_df['x'].copy()
pass_df['x'] = 68 - pass_df['y']
pass_df['y'] = temp

temp = pass_df['endX'].copy()
pass_df['endX'] = 68 - pass_df['endY']
pass_df['endY'] = temp

## subplots
fig, ax = plt.subplots(figsize=(8, 12.5), facecolor="#222222")
ax.set_facecolor("#222222")

## name of the plot
name = "plots/Barcelona/La_Liga/2020_21/03_barca_v_sevilla/coutinho/08_prog_passes.jpg"

## init object of Pass class
pass_obj = pass_utils.Pass(
    pitch_color="#222222", orientation="vertical",
    radius=0.8, circle_fc="#efaa42", circle_alpha=0.8,
    circle_ec="#121212", circle_fc_uns="#222222", circle_alpha_uns=1,
    circle_ec_uns="#9F9F9F", tri_fc_uns="#9F9F9F", tri_alpha_uns=0.7, 
    tri_fc="#efaa42", tri_alpha=0.3)
fig, ax = pass_obj.plot_passes(
    pass_df, pass_type="progressive_passes",
    save_path=name, image_path="logos/fcb.png",
    orientation_array=[0.15, 0.83, 0.07, 0.05], main_title=f"{player_name} - Progressive Passes",
    sub_title="La Liga | Season 2020/2021", credit="created by @slothfulwave612", figax=(fig, ax),
    main_size=19, sub_size=15, credit_size=8,
    main_coord=(9,109), sub_coord=(9,106), credit_coord=(68,-1), font="Gayathri"
)

## -------------- Progressive Passes --------------

## -------------- Defensive heatma --------------

## create touch dataframe
# def_df = event_df.loc[
#     (
#         (event_df["type_displayName"] == "Aerial") |
#         (event_df["type_displayName"] == "Tackle") |
#         (event_df["type_displayName"] == "Challenge") |
#         (event_df["type_displayName"] == "Clearance") |
#         (event_df["type_displayName"] == "Interception") |
#         (event_df["type_displayName"] == "BlockedPass") |
#         (event_df["type_displayName"] == "Foul")   
#     ) & 
#     (event_df["playerId"] == 80767)
# ].copy()

# ## cmap
# cmap = ["#222222", "#2D2424", "#382626", "#432828", "#4D2929", "#632C2C", "#6E2E2E", "#843131", "#993434", "#A33535", "#AE3737", "#B93838", "#CE3B3B"]

# name = "plots/Barcelona/La_Liga/2020_21/03_barca_v_sevilla/coutinho/11_heatmap.jpg"

# ## init object of Pitch class
# fig, ax = plt.subplots(figsize=(12,8), facecolor="#222222")
# ax.set_facecolor("#222222")

# ## init object of Defence class
# defence = defence_utils.Defence(
#     orientation="horizontal", zorder=4, scatter_size=100, succ_color="#EFAA42", unsucc_color="#9F9F9F"
# )
# fig, ax = defence.plot_defensive(def_df, def_type="all_def_activity", figax=(fig,ax))

# # init object of heatmap class
# heat_obj = heatmap.Heatmap(
#     line_color="#ececec", pitch_color="#222222", cmap=cmap, show=False, interpolation="none"
# )
# fig, ax = heat_obj.make_heatmap(
#     def_df, heat_type="simple_heatmap", bins=(10,10), filename=name, image_path="logos/fcb.png",
#     orientation_array=[-0.04, 0.83, 0.4, 0.07], main_title=f"{player_name} - Defensive Actions",
#     sub_title="La Liga | Season 2020/2021", credit="created by @slothfulwave612", figax=(fig, ax),
#     main_size=19, sub_size=15, credit_size=8,
#     main_coord=(7,73), sub_coord=(7,70), credit_coord=(103.5,1), font="Gayathri"
# )

'''
def add_title(self, fig, text_dict, image, **kwargs):
        """
        Args:
            fig (figure.Figure): figure object.
            text_dict (dict): containing text to be plotted.
            image (str): path where image is saved.
            **kwargs : All other keyword arguments are passed on to matplotlib.axes.Axes.text.

        Returns:
            figure.Figure: figure object.
            axes.Axes: axes object.
        """        
        # title list
        text_list_fig = [
            dict(x=0.21, y=0.775, s=text_dict["title"], size=26, **kwargs),
            dict(x=0.21, y=0.755, s=text_dict["sub_title"], size=20, **kwargs),
            dict(x=0.889, y=0.765, s=text_dict["logo"], size=24, ha="right", **kwargs),
        ]

        # plot text
        for text in text_list_fig:
            my_utils.plot_text_fig(fig, self.pitch_color, **text)

        # add image
        if image is not None:
            fig = my_utils.add_image(
                image, fig, 0.135, 0.735, 0.07, 0.07
            )

        return fig
    
    def add_credits(self, fig, text_dict, **kwargs):
        """
        Args:
            fig (axes.Axes): figure object.
            text_dict (dict): containing text to be plotted.
            **kwargs : All other keyword arguments are passed on to matplotlib.axes.Axes.text.

        Returns:
            figure.Figure: figure object.
            axes.Axes: axes object.
        """        
        # title list
        text_list_fig = [
            dict(x=0.889, y=0.22, s=text_dict["credit_right"], size=12, ha="right", **kwargs),
            dict(x=0.137, y=0.22, s=text_dict["credit_left"], size=12, **kwargs),
        ]

        # plot text
        for text in text_list_fig:
            my_utils.plot_text_fig(fig, self.pitch_color, **text)

        return fig
'''