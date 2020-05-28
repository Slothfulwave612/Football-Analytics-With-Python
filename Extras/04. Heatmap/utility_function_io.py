# -*- coding: utf-8 -*-
"""
Created on Thu May 28 22:59:16 2020

@author: slothfulwave612

Python module for i/o operations.

Modules Used(2):-
1. pandas -- data manipulation and analysis library.
2. json -- Python library to work with JSON data.
"""

import pandas as pd
from pandas.io.json import json_normalize
import json

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

def required_events(event_df, player):
    '''
    Function for making event dataframe for the specified player.
    
    Arguments:
    event_df -- dataframe object, containing event data.
    player -- str, the player name
    
    Returns:
    req_event -- dataframe object containing event data for the required player.
    '''
    req_event = event_df.loc[event_df['player_name'] == player].copy()
    
    return req_event

















