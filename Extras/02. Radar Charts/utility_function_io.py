# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:27:19 2020

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

def convert_to_per_90(stats, minutes_played):
    '''
    Function to convert to per 90.
    
    Arguments:
    stats -- int, statistics that we have to change to per 90.
    minutes_played -- int, minutes played by the player.
    '''
    return round( (stats / minutes_played) * 90, 2)

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

def make_event_df(match_id):
    '''
    Function for making event dataframe for given match id.
    
    Argument:
    match_id -- int, the required match id for which event data will be extracted.
    
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

def get_shot_stats(event_df, player_name, min_played):
    '''
    Function to get non-penalty goals, total number of shots by the player,
    shots on target and the shooting percentage.
    
    Arguments:
    event_df -- dataframe object, containing event data.
    player_name -- str, the player name.
    min_played -- int, minutes played by the player.
    
    Returns:
    goals -- int, non-penalty goals.
    shots -- float, shots taken by the player(per 90).
    shots_on_target -- int, shots that were on target.
    shooting_per -- float, shooting percentage.
    '''
    goals = sum( (event_df['player_name'] == player_name) & 
                 (event_df['type_name'] == 'Shot') & 
                 (event_df['shot_type_name'] != 'Penalty') & 
                 (event_df['shot_outcome_name'] == 'Goal') )
    ## total number of non-penalty shots
    
    shots = sum( (event_df['player_name'] == player_name) & 
                 (event_df['type_name'] == 'Shot') )
    ## total number of shots taken by the player
    
    shots_on_target = sum( (event_df['player_name'] == player_name) & 
                           (event_df['type_name'] == 'Shot') & 
                           ( (event_df['shot_outcome_name'] == 'Goal') | 
                             (event_df['shot_outcome_name'] == 'Saved') | 
                             (event_df['shot_outcome_name'] == 'Saved to Post') ) )
    ## shots by the player that were on target
    
    shooting_per = round( (shots_on_target / shots) * 100, 2 )
    ## calculating shooting percentage, 2 decimal places
    
    shots = convert_to_per_90(shots, min_played)
    ## converting to per_90
    
    return goals, shots, shots_on_target, shooting_per

def get_pass_stats(event_df, player_name, min_played):
    '''
    Function to get passing percentage, assists, key passes and
    through balls.
    
    Arguments:
    event_df -- dataframe object, contains event data.
    player_name -- str, the player name.
    min_played -- int, minutes played by the player.
    
    Returns:
    pass_per -- float, passing percentage.
    assist -- float, total number of assists(per 90). 
    key_pass -- float, total number of key passes(per 90).
    through_ball -- float, total number of thorugh balls(per 90).
    '''
    tot_pass = sum( (event_df['player_name'] == player_name) & 
                    (event_df['type_name'] == 'Pass') ) 
    ## total passes by the player
    
    succ_pass = sum( event_df.loc[ (event_df['player_name'] == player_name) & 
                              (event_df['type_name'] == 'Pass'), 'pass_outcome_name' ].isna() )
    ## successful passes by the player
    
    pass_per = round( (succ_pass / tot_pass) * 100, 2)
    ## calculating passing percentage
    
    assist = sum( (event_df['player_name'] == player_name) & 
                  (event_df['type_name'] == 'Pass') & 
                  (event_df['pass_goal_assist'] == True) )
    ## assist by the player
    
    key_pass = sum( (event_df['player_name'] == player_name) & 
                    (event_df['type_name'] == 'Pass') & 
                    (event_df['pass_shot_assist'] == True))
    ## key passes by the player
    
    through_ball = sum( (event_df['player_name'] == player_name) & 
                        (event_df['type_name'] == 'Pass') & 
                        (event_df['pass_technique_name'] == 'Through Ball'))    
    ## through balls by the player
    
    assist = convert_to_per_90(assist, min_played)
    key_pass = convert_to_per_90(key_pass, min_played)
    through_ball = convert_to_per_90(through_ball, min_played)
    ## converting to per_90
    
    return pass_per, assist, key_pass, through_ball

def succ_dribbles(event_df, player_name, min_played):
    '''
    Function to count successful dribbles.
    
    Arguments:
    event_df -- dataframe object, containing event data.
    player_name -- str, the player name.
    min_played -- int, minutes played by the player.
    
    Returns:
    dribbles -- float, dribble(per 90) count.
    '''
    dribbles = sum( (event_df['player_name'] == player_name) & 
                    (event_df['type_name'] == 'Dribble') & 
                    (event_df['dribble_outcome_name'] == 'Complete') )
    ## total number of dribbles by the player
    
    dribbles = convert_to_per_90(dribbles, min_played)
    
    return dribbles
