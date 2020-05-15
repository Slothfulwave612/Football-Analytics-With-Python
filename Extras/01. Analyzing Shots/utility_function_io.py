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

import pandas as pd
from pandas.io.json import json_normalize
import datetime
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
    Function for making event dataframe for given match id.
    
    Argument:
    match_id -- int, the required match id for which event data will be extracted.
    
    Returns:
    event_df -- dataframe object, the event dataframe for the particular match.
    '''
    ## setting path for the required file
    path = '../Statsbomb/data/events/{}.json'.format(match_id)
    
    ## reading in the json file
    event_json = json.load(open(path, encoding='utf-8'))    

    ## normalize the json data
    df = json_normalize(event_json, sep='_')
    
    return df

def convert_to_datetime(df):
    '''
    Function to convert a string pandas series to datetime object.
    
    Argument:
    df -- dataframe object.
    
    Returns:
    df -- dateframe object.
    '''
    df['match_date'] = pd.to_datetime(df['match_date'])
    
    return df

def get_selected_match(match_df, start_date, end_date):
    '''
    Function to get only those matches between start_date and end_date.
    
    Arguments:
    match_df -- dataframe object, containing matches.
    start_date -- str, the starting date(YYYY-MM-DD).
    end_date -- str, the ending date(YYYY-MM-DD).
    
    Returns:
    requied_df -- dataframe object, containing required rows.
    '''
    ## start date
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")    
    
    mask = (match_df['match_date'] > start_date) & (match_df['match_date'] <= end_date)
    
    required_df = match_df.loc[mask].copy()
    
    return required_df

def get_selected_events(scoring_df_ids):
    '''
    Function for making a dataframe which will have events for all the matches.
    
    Arguments:
    scoring_df_ids -- list, containing all required match ids.
    
    Returns:
    scoring_events -- dataframe object, containing all the required events.
    '''
    c = 0
    
    for match_id in scoring_df_ids:
        temp_df = make_event_df(match_id)
        
        temp_shot = temp_df.loc[
                (temp_df['type_name'] == 'Shot') & (temp_df['player_name'] == 'Lionel Andrés Messi Cuccittini')
                ].copy()
        
        if c == 0:
            shots_df = temp_shot
            c += 1
        else:
            shots_df = pd.concat([shots_df, temp_shot], sort=True)
    
    return shots_df
                    
