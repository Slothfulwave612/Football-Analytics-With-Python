# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:27:19 2020

@author: slothfulwave612

Python module for i/o operations.

Modules Used(3):-
1. numpy -- numerical computing library.
2. pandas -- data manipulation and analysis library.
3. json -- Python library to work with JSON data.
"""

import numpy as np
import pandas as pd
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
    matches_df -- dataframe object, containing all the matches 
    '''
    ## setting path to the file
    path = '../Statsbomb/data/matches/{0}/{1}.json'.format(comp_id, season_id)
    
    ## loading up the data from json file
    match_data = json.load(open(path))
    
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
    Function for making event dataframe and return the linups as well.
    
    Argument:
    match_id -- int, the required match id for which event data will be constructed.
    
    Returns:
    event_df -- dataframe object, the event dataframe for the particular match.
    lineups -- lineups for the match.
    '''
    ## setting path for the required file
    path = '../Statsbomb/data/events/{}.json'.format(match_id)
    
    ## reading in the json file
    event_json = json.load(open(path, encoding='utf-8'))
    
    ## lineups for the game
    lineups = event_json[0:2]
    
    return event_json[4:], lineups

def get_straters(lineup):
    '''
    Function for getting the player's name and their jersey numbers.
    
    Argument:
    lineup -- dict, containing the team lineup data.
    
    Returns:
    players -- dict, containing player id as key and name, jersey number as its value(nested dict)        
    '''
    players = {p['player']['id']: {'name': p['player']['name'],
                                  'jersey': p['jersey_number']} for p in lineup['tactics']['lineup']}
    
    return players
    
def passing_matrix(pass_data):
    '''
    Function to make a passing matrix, it will contain the total number 
    of passes from player_A to player_B.
    
    Argument:
    pass_data -- dict, containing passing data for a team.
    
    Returns:
    pass_matrix -- matrix containing total number of passes between each players.
    '''
    ## initialize a pass matrix as an empty dictionary
    pass_matrix = {}
    
    for pdata in pass_data:
        if 'outcome' not in pdata['pass'].keys():
            passer_id = pdata['player']['id']
            recipient_id = pdata['pass']['recipient']['id']
            
            a, b = sorted([passer_id, recipient_id])
            
            if pass_matrix.get(a) == None:
                pass_matrix[a] = {}
            
            if pass_matrix[a].get(b) == None:
                pass_matrix[a][b] = 0
            
            pass_matrix[a][b] += 1
    
    return pass_matrix


def get_avg_player_pos(event, players):
    '''
    Function to get average position for each player.
    
    Argumrnts:
    event -- dict, containing event data for a team.
    players -- dict, containing starting XI.
    
    Returns:
    avg_position -- dict, containing avg position for each player.
    '''
    ## initializing a position matrix as empty dictionary
    position_matrix = {}
    
    for e in event:
        if e.get('player') != None:
            player_id = e['player']['id']
            
            if position_matrix.get(player_id) == None:
                position_matrix[player_id] = {'x': [], 'y': []}
            
            if e.get('location') != None:
                position_matrix[player_id]['x'].append(e['location'][0])
                position_matrix[player_id]['y'].append(80 - e['location'][1])
    
    avg_position = {k: [np.mean(v['x']), np.mean(v['y'])] 
                                    for k, v in position_matrix.items() if k in players.keys()}
    
    return avg_position

def vol_passes_exchanged(pass_matrix, players, avg_position):
    '''
    Function to get volume of passes exchanged between each player.
    
    Arguments:
    pass_matrix -- matrix containing total number of passes between each players.
    players -- dict, containing starting XI.
    avg_position -- dict, containing avg position for each player.
    
    Returns:
    lines -- containing the x and y position for two players between which passes were made.
    weights -- containing the number of passes between the two players.
    '''
    lines = []
    weights = []
    
    for k, v in pass_matrix.items():
        if players.get(k) != None:
            origin = avg_position[k]
            
            for k_, v_ in pass_matrix[k].items():
                if players.get(k_) != None:
                    dest = avg_position[k_]
                    lines.append([*origin, *dest])
                    weights.append(v_)
    
    return lines, weights
