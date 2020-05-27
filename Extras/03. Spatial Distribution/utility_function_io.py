# -*- coding: utf-8 -*-
"""
Created on Tue May 26 01:24:36 2020

@author: slothfulwave612

Python module for i/o operations.

Modules Used(4):-
1. numpy -- numerical computing library.
2. pandas -- data manipulation and analysis library.
3. json -- Python library to work with JSON data.
4. sklearn -- machine learning library for the Python programming language.
"""

import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import json
from sklearn.decomposition import NMF

def get_competitions():
    '''
    Function for getting information about each and every
    competitions.
    
    Returns:
    comp_df -- dataframe for competition data.
    '''
    comp_data = json.load(open('../Statsbomb/data/competitions.json'))
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

def get_matches(comp_id, season_id):
    '''
    Function for getting matches for the given
    competition id.
    
    Arguments:
    comp_id -- int, the competition id.
    season_id -- int, the season id.
    
    Returns:
    match_df -- dataframe object, containing all the matches 
    '''
    ## setting path to the file
    path = '../Statsbomb/data/matches/{0}/{1}.json'.format(comp_id, season_id)
    
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
        
        
def getting_match_id(match_df, req_home_team, req_away_team):
    '''
    Function for getting required match id.
    
    Arguments:
    match_df -- dataframe object, representing the match dataframe.
    req_home_team -- str, required home team.
    req_away_team -- str, required away team.
    
    Returns:
    match_id -- int, the required match id.
    '''

    for row_num, match in match_df.iterrows():
        home_team = match['home_team_name']
        away_team = match['away_team_name']
        
        if home_team == req_home_team and away_team == req_away_team:
            match_id_required = match['match_id']

    return match_id_required

def get_req_matches(comp_id, season_list, team_1, team_2):
    '''
    Function to get required match ids for particular seasons.
    
    Arguments:
    comp_id -- int, competition id.
    season_list -- list, containing season ids.
    team_1 -- str, first team name.
    team_2 -- str, second team name.
    
    Returns:
    match_ids -- dict, containing season_id -> match_id 
                       as key -> value pair.
    '''
    match_dict = {}
    match_ids = {}
    
    for season_id in season_list:
        match_info = get_matches(comp_id, season_id)
        match_dict[season_id] = match_info
        
        if season_id == 41:
            home_team = team_2
            away_team = team_1
        else:
            home_team = team_1
            away_team = team_2
        
        match_ids[season_id] = getting_match_id(match_info, home_team, away_team)
    
    return match_ids

def make_event_df(match_id):
    '''
    Function for making event dataframe.
    
    Argument:
    match_id -- int, the required match id for which event data will be constructed.
    
    Returns:
    event_df -- dataframe object, the event dataframe for the particular match.
    '''
    ## setting path for the required file
    path = '../Statsbomb/data/events/{}.json'.format(match_id)
    
    ## reading in the json file
    event_json = json.load(open(path, encoding='utf-8'))[2:]
    
    ## normalize the json data
    df = json_normalize(event_json, sep='_')
    
    return df


def get_required_events(player_list, match_id):
    '''
    Function to make event dataframe for only the specified players.
    
    Arguments:
    player_list -- list, of players.
    match_id -- int, match id.
    
    Returns:
    required_df -- dataframe object.
    '''
    df = make_event_df(match_id)
    
    required_df = df.loc[df['player_name'].isin(player_list)]
    
    return required_df

def make_lists(x_scale, y_scale):
    '''
    Function to return the required lists.
    
    Arguments:
    x_scale -- int, size of list
    y_scale -- int, size of list
    
    Returns:
    x_bins, y_bins -- required lists.
    '''
    x_bins = np.linspace(0, 120, x_scale)
    y_bins = np.linspace(0, 80, y_scale)
    
    return x_bins, y_bins

def cumulative_actions(messi_df, x_scale, y_scale, x_bins, y_bins):
    '''
    Function to populate the player dictionary with a matrix that represents spatially
    distributed cumulative actions a player generate in the dataset.
    
    Arguments:
    messi_df -- dataframe object, containing the event data.
    x_scale -- int, size of x_bins.
    y_scale -- int, size of y_bins.
    x_bins -- list
    y_bins -- list
    
    Returns:
    player -- matrix
    '''
    players = {}
    
    for row_num, data in messi_df.iterrows():
        player_id = data['player_id']
        
        if players.get(player_id) is None:
            players[player_id] = np.zeros((x_scale, y_scale))
        
        try:
            x_bin = int(np.digitize(data['location'][0], x_bins[1:], right=True))
            y_bin = int(np.digitize(data['location'][1], y_bins[1:], right=True))
            players[player_id][x_bin][y_bin] += 1
        except:
            pass
    
    return players

def non_neg_matrix_factorization(player):
    '''
    Function to build a model using the NMF class, and fit it by feeding 
    player matrix into fit_transform.
    
    Argument:
    player -- dict
    
    Return:
    model_dict -- NMF model dict.
    '''
    model_dict = {}

    for key, value in player.items():
        player = [np.matrix.flatten(value)]
    
        comps = 30
    
        model = NMF(n_components=comps, init='random', random_state=0)
    
        model.fit(player)
        
        model_dict[key] = model
    
    return model_dict
      