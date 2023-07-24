"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module containing utility functions.
"""

import math
import json
import numpy as np
import pandas as pd
from pandas import json_normalize
from PIL import Image
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import matplotlib.font_manager as fm
import matplotlib.patheffects as path_effects

class FontManager:
    """Utility to load fun fonts from https://fonts.google.com/ for matplotlib.
    Find a nice font at https://fonts.google.com/, and then get its corresponding URL
    from https://github.com/google/fonts/.
    The FontManager is taken from the ridge_map package by Colin Carroll (@colindcarroll).
    Parameters
    ----------
    url : str, default is the url for Roboto-Regular.ttf
        Can really be any .ttf file, but probably looks like
        'https://github.com/google/fonts/blob/master/ofl/cinzel/static/Cinzel-Regular.ttf?raw=true'
        Note make sure the ?raw=true is at the end.
    Examples
    --------
    >>> from mplsoccer import FontManager
    >>> import matplotlib.pyplot as plt
    >>> font_url = 'https://github.com/google/fonts/blob/master/ofl/abel/Abel-Regular.ttf?raw=true'
    >>> fm = FontManager(url=font_url)
    >>> fig, ax = plt.subplots()
    >>> ax.text("Good content.", fontproperties=fm.prop, size=60)
    """

    def __init__(self,
                 url=('https://github.com/google/fonts/blob/master/'
                      'apache/roboto/static/Roboto-Regular.ttf?raw=true')):
        self.url = url
        with NamedTemporaryFile(delete=False, suffix=".ttf") as temp_file:
            temp_file.write(urlopen(self.url).read())
            self._prop = fm.FontProperties(fname=temp_file.name)

    @property
    def prop(self):
        """Get matplotlib.font_manager.FontProperties object that sets the custom font."""
        return self._prop

    def __repr__(self):
        return f'{self.__class__.__name__}(font_url={self.url})'


def get_competition(path):
    '''
    Function for getting data about all the competitions.
    Argument:
        path -- str, path to competition.json file.
    Returns:
        comp_df -- pandas dataframe, all competition data.
    '''
    ## load the json file
    comp_data = json.load(open(path))

    ## make pandas dataframe
    comp_df = pd.DataFrame(comp_data)

    return comp_df

def flatten_json(sub_str):
    '''
    Function to take out values from nested dictionary present in 
    the json file, so to make a representable dataframe.
    
    ---> This piece of code was found on stackoverflow <--
    
    Argument:
        sub_str -- substructure defined in the json file.
    
    Returns:
        flattened out information.
    '''
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(sub_str)
    
    return out

def get_matches(path):
    '''
    Function for getting match-data for a given competition
    
    Arguments:
        path -- str, path to .json file containing match data (matches/comp_id/season_id.json).
    
    Returns:
        match_df -- pandas dataframe, containing all the matches 
    '''    
    ## loading up the data from json file
    match_data = json.load(open(path, encoding='utf8'))
    
    ## flattening the json file
    match_flatten = [flatten_json(x) for x in match_data]
    
    ## creating a dataframe
    match_df = pd.DataFrame(match_flatten)
    
    match_df_cols = list(match_df.columns)
    
    ## renaming the dataframe
    for i in range(len(match_df_cols)):
        if match_df_cols[i].count('away_team') == 2:
            ## for away_team columns
            match_df_cols[i] = match_df_cols[i][len('away_team_'):]
        
        elif match_df_cols[i].count('_0') == 1:
            ## for _0 columns
            match_df_cols[i] = match_df_cols[i].replace('_0', '')
        
        elif match_df_cols[i].count('competition') == 2:
            ## for competition columns
            match_df_cols[i] = match_df_cols[i][len('competition_'):]
        
        elif match_df_cols[i].count('home_team') == 2:
            ## for away_team columns
            match_df_cols[i] = match_df_cols[i][len('home_team_'):]
        
        elif match_df_cols[i].count('season') == 2:
            ## for away_team columns
            match_df_cols[i] = match_df_cols[i][len('season_'):]

    match_df.columns = match_df_cols 
        
    return match_df

def get_shots(match_id):
    '''
    Function for making shots dataframe.
    
    Args:
        match_id (int): file name where data is present
    
    Returns:
        pandas dataframe: the shot dataframe for the particular match.
    '''
    # path for shots
    path_shots = f"../data/xg_events/{match_id}.json"

    # read in the json file
    shots_json = json.load(open(path_shots, encoding='utf-8'))

    # home and away team shots
    shots_h = pd.DataFrame(shots_json['h'])
    shots_a = pd.DataFrame(shots_json['a'])

    # main df
    shots_df = pd.concat([shots_h, shots_a]).reset_index(drop=True).sort_values(by="minute", ascending=True)

    # change the dtype
    shots_df['X'] = shots_df['X'].astype(float)
    shots_df['Y'] = shots_df['Y'].astype(float)
    shots_df["xG"] = shots_df["xG"].astype(float)

    # convert coordinates
    # shots_df['X'] = shots_df['X'].apply(lambda x: change_dims(x, 0, 1, 0, 104))
    # shots_df['Y'] = shots_df['Y'].apply(lambda y: change_dims(y, 0, 1, 0, 68))

    return shots_df

def make_event_df(match_id):
    '''
    Function for making event dataframe.
    
    Args:
        match_id (int): file name where data is present
    
    Returns:
        pandas dataframe: the event dataframe for the particular match.
    '''
    ## path for event and rest
    path_event = f"../data/events/{match_id}.json"
    path_rest = f"../data/rest/{match_id}.json"
    path_lineup = f"../data/lineups/{match_id}.json"

    ## read in the json file
    event_json = json.load(open(path_event, encoding='utf-8'))
    event_df = json_normalize(event_json, sep='_')

    ## read in the json file -- rest.json
    rest_json = json.load(open(path_rest, encoding="utf-8"))

    ## dict for team ids
    team_dict = {
        rest_json["home"]["teamId"]: rest_json["home"]["name"],
        rest_json["away"]["teamId"]: rest_json["away"]["name"]
    }

    ## fill teamId as team-names
    event_df["teamId"] = event_df["teamId"].map(team_dict)

    ## read the lineups
    lineup_json = json.load(open(path_lineup, encoding="utf-8"))

    ## fill na in playerId column
    event_df["playerId"].fillna(0,inplace=True)

    ## convert playerId column from float to int
    event_df["playerId"] = event_df["playerId"].astype(int).astype(str)

    ## change id to names
    event_df["playerId"] = event_df["playerId"].map(lineup_json)

    ## rename teamId to team_name
    event_df = event_df.rename(
        columns={
            "teamId": "team_name",
            "playerId": "player_name"
        }
    )

    # convert coordinates
    # event_df = convert_coord(event_df)

    return event_df

def change_dims(old_value, old_min, old_max, new_min, new_max):
    """
    Function for changing the coordinates to our pitch dimensions.

    Args:
        old_value (float): the original coordinate value
        old_min (float): the min value of the original pitch range.
        old_max (float): the max value of the original pitch range.
        new_min (float): the min value of our pitch range.
        new_max (float): the max value of the our pitch range.

    Returns:
        float: the converted coordinate value.
    """    
    ## calculate the value
    new_value = ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

    return new_value

def get_indices(width, height, x_partition, y_partition, xinput, yinput):
    """
    Function for getting index values for matrix

    Args:
        width (float): width of the pitch.
        height (float): height of the pitch.
        x_partition (int): number of partitions in horizontal axis.
        y_partition (int): number of partitions in vertical axis.
        xinput (float): x-coodinate value.
        yinput (float): y-coordinate value.

    Returns:
        tuple: containning indices for matrix
    """    
    x_step = width / x_partition
    y_step = height / y_partition
    x = math.ceil((xinput if xinput > 0 else 0.5) / x_step) # handle border cases as well
    y = math.ceil((yinput if yinput > 0 else 0.5) / y_step)  # handle border cases as well
    return y_partition - y, x - 1

def convert_coord(df):
    """
    Function for converting passing coordinate information to our pitch dimensions.

    Args:
        df (pandas.DataFrame): required dataframe
    
    Returns:
        pandas.DataFrame: dataframe with converted coordinates.
    """    
    ## convert the coordinates
    df['x'] = df['x'].apply(lambda x: change_dims(x, 0, 100, 0, 104))
    df['y'] = df['y'].apply(lambda y: change_dims(y, 0, 100, 0, 68))
    df['endX'] = df['endX'].apply(lambda x: change_dims(x, 0, 100, 0, 104))
    df['endY'] = df['endY'].apply(lambda y: change_dims(y, 0, 100, 0, 68))

    return df

def disance_sqr(point_1, point_2):
    """
    Function to calculate distance between two coordinates.

    Args:
        point_1 (tuple): containing x and y coordinate.
        point_2 (tuple): containing x and y coordinate.

    Returns:
        float: distance square
    """   
    return (point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2

def load_team_season(match_id_array):
    """
    Function to load all events of a team
    given match-ids.

    Args:
        match_id_array (list/numpy.array): containing match-ids.
    
    Returns:
        pandas.DataFrame: containing event data.
    """   
    ## init an empty pandas dataframe
    event_df = pd.DataFrame()

    ## iterate match-id array
    for match_id in match_id_array:

        ## get event data for a particular match
        temp_df = make_event_df(match_id)

        ## concat the dataframes
        event_df = pd.concat(
            [event_df, temp_df], axis=0
        )
    
    ## reset the index
    event_df = event_df.reset_index(drop=True)

    return event_df

def key_assist(qualifier):
    """
    Function to find key-pass and assists.

    Args:
        qualifier (list): containing pass info

    Returns:
        str: type of pass.
    """    
    key_pass = 0
    
    for i in qualifier:
        if i["type"]["displayName"] == "IntentionalGoalAssist":
            return "Assist"
        elif i["type"]["displayName"] == "ShotAssist":
            key_pass = 1
        
    if key_pass == 1:
        return "Key Pass"
    elif key_pass == 0:
        return "Simple Pass"

def is_free_kick(qualifier):
    for i in qualifier:
        if i["type"]["displayName"].lower() in ["freekicktaken", "indirectfreekicktaken", "directfreekick"]:
            return True
    return False

def is_goal_kick(qualifier):
    for i in qualifier:
        if i["type"]["displayName"] in ["GoalKick", "KeeperThrow", "ThrowIn", "StandingSave"]:
            return True
    return False

def plot_text_ax(ax, foreground, width=3, **kwargs):
    """
    Function to plot text on axes.
    """
    text = ax.text(
        **kwargs
    )
    text.set_path_effects(
        [path_effects.withStroke(linewidth=width, foreground=foreground)]
    )

def plot_text_fig(fig, foreground, **kwargs):
    """
    Function to plot text on axes.
    """
    text = fig.text(
        **kwargs
    )
    text.set_path_effects(
        [path_effects.withStroke(linewidth=3, foreground=foreground)]
    )

def swap(df):
    """
    Swap x and y values for vertical pitch.

    Args:
        df (pandas.DataFrame): required dataframe.

    Returns:
        pandas.DataFrame: with swapped columns.
    """
    m = pd.to_numeric(df['x']).notna()

    df.loc[m,['x','y']] = df.loc[m,['y','x']].values
    df.loc[m,['endX','endY']] = df.loc[m,['endY','endX']].values
    
    df['endX'] = 100 - df['endX']
    df['x'] = 100 - df['x']

    return df

def swap_shot(df):
    """
    Swap x and y values for vertical pitch.

    Args:
        df (pandas.DataFrame): required dataframe.

    Returns:
        pandas.DataFrame: with swapped columns.
    """
    m = pd.to_numeric(df['X']).notna()

    df.loc[m,['X','Y']] = df.loc[m,['Y','X']].values
    
    df['X'] = 68 - df['X']

    return df


def cal_time(event, index):
    return (event.loc[index, "minute"] * 60) + event.loc[index, "second"]