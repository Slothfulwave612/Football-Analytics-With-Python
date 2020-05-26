# -*- coding: utf-8 -*-
"""
Created on Tue May 26 01:24:36 2020

@author: slothfulwave612

Python module for i/o operations.

Modules Used(3):-
1. numpy -- numerical computing library.
2. pandas -- data manipulation and analysis library.
3. json -- Python library to work with JSON data.
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
    matches_df -- dataframe object, containing all the matches 
    '''
    ## setting path to the file
    path = '../Statsbomb/data/matches/{0}/{1}.json'.format(comp_id, season_id)
    
    ## loading up the data from json file
    match_data = json.load(open(path, encoding='utf8'))
    
    ## flattening the json file
    match_flatten = [flatten_json(x) for x in match_data]
    
    ## creating a dataframe
    match_df = pd.DataFrame(match_flatten)
    
    return match_df

def renaming_columns(match_df_cols):
    '''
    Function for renaming match dataframe columns.
    
    Argument:
    match_df_cols -- columns of match dataframe.
    
    Returns:
    match_df_cols -- list with renamed column names.
    '''
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
        
    return match_df_cols
        
        
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


def get_season_events(comp_id, match_ids):
    '''
    Function for getting all events for each matches played in the season.
    
    Arguments:
    comp_id -- int, competition id.
    match_ids -- list, of match id.
    
    Returns:
    event_df -- dataframe object.
    '''
    c = 0
    
    for match_id in match_ids:
        temp_df = make_event_df(match_id)
        
        if c == 0:
            event_df = temp_df
            c = 1
        else:
            event_df = pd.concat([event_df, temp_df], sort=True)

    return event_df  

def make_messi_events(event_df):
    '''
    Function for making event dataframe for Lionel Messi.
    
    Argument:
    event_df -- dataframe object, containing event data.
    
    Returns:
    messi_df -- dataframe object, containing event data of Lionel Messi.
    '''
    messi_df = event_df.loc[event_df['player_name'] == 'Lionel Andrés Messi Cuccittini']
    
    return messi_df

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
    player = np.zeros((x_scale, y_scale))
    
    for row_num, data in messi_df.iterrows():
        try:
            x_bin = int(np.digitize(data['location'][0], x_bins[1:], right=True))
            y_bin = int(np.digitize(data['location'][1], y_bins[1:], right=True))
            player[x_bin, y_bin] += 1
        except:
            pass
    
    return player

def non_neg_matrix_factorization(player):
    '''
    Function to build a model using the NMF class, and fit it by feeding 
    player matrix into fit_transform.
    
    Argument:
    player -- matrix
    
    Return:
    model -- NMF model.
    '''
    player = [np.matrix.flatten(player)]
    
    comps = 30
    
    model = NMF(n_components=comps, init='random', random_state=0)
    
    model.fit(player)
    
    return model












            