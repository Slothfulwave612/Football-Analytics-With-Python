"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module for corner utils.
"""
def is_corner_(qualifier):
    for i in qualifier:
        if i["type"]["displayName"] == "CornerTaken":
            return True
    return False

def is_corner(x):
    x_coord, qualifier = x

    for i in qualifier:
        if i["type"]["displayName"] == "CornerTaken":
            if x_coord < 1:
                return "Left Corner"
            elif x_coord > 67:
                return "Right Corner"
    return False

def corner_info(x):
    """
    Function to return the outcome of corners.

    Args:
        x (pandas.Series): required values
    """
    outcome, pass_type = x

    if pass_type == "Simple Pass":
        return outcome
    elif pass_type == "Key Pass":
        return "Shot"
    elif pass_type == "Assist":
        return "Goal"

"""
# shot_df = pd.DataFrame()

# traverse the match ids
# for match_id in tqdm(match_ids, total=len(match_ids)):
#     event = my_utils.make_event_df(match_id)

#     event = my_utils.swap(event)

#     event["is_corner"] = event[['x', "qualifiers"]].apply(
#         lambda x: corner_utils.is_corner(x), axis=1
#     )

#     corner_index = event.loc[
#         (event["team_name"] != "Barcelona") &
#         (event["is_corner"] != False)
#     ].index

#     shot_index = []

#     for index in corner_index:
#         curr_time = my_utils.cal_time(event, index)
#         temp_index = index + 1
#         corner_side = event.loc[index, "is_corner"]

#         while my_utils.cal_time(event, temp_index) - curr_time <= 10:
#             if event.loc[temp_index, "is_corner"] != False:
#                 break

#             elif event.loc[temp_index, "isShot"] == True:
#                 event.loc[temp_index, "is_corner"] = corner_side
#                 shot_index.append(temp_index)

#             temp_index += 1
    
#     shot_df = pd.concat([shot_df, event.loc[shot_index]])

# shot_df = shot_df.reset_index(drop=True)

# shot_df.to_pickle("../_data_/barca/corners_shots.pkl")

#########################################################################

# init empty dataframe
# corner_data = []

# # traverse the match ids
# for match_id in tqdm(match_ids, total=len(match_ids)):
#     event = my_utils.make_event_df(match_id)

#     event = my_utils.swap(event)

#     event["is_corner"] = event[['x', "qualifiers"]].apply(
#         lambda x: corner_utils.is_corner(x), axis=1
#     )

#     indices = event.loc[
#         (event["team_name"] != team) &
#         (event["is_corner"] != False)
#     ].index

#     for index in indices:
#         corner_side = event.loc[index, "is_corner"]
#         event.loc[index + 1, "is_corner"] = corner_side
#         corner_data.append(event.loc[index + 1])
    
# corner_df = pd.DataFrame(corner_data).reset_index(drop=True)

# corner_df.to_pickle("../_data_/barca/corners.pkl")
"""