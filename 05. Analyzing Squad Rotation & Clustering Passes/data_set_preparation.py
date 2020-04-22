# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:42:31 2020

@author: slothfulwave612

This Python module will prepare the data set by 
extracting the data we need and then by performing 
cleaning. We will store the dataset in .csv format
so that we can use it for our main analysis

Modules Used(2):
----------------
1. json -- module used for the manipulation of JSON files.
2. pandas -- Python library for data analysis.
"""
import json 
import pandas as pd
import utility_io_viz as uiv

## obtaining competitons
## reading the json file
competition = json.load(open('../Statsbomb/data/competitions.json'))

## converting the list 'competition' into dataframe
df = pd.DataFrame(competition)

## path where all matches files are stored
path = '../Statsbomb/data/matches'       

## calling the function to get the list of path to all the matches json files
file_path_matches = uiv.find_json(path, name='matches')

## creating an empty list which will contain dataframe for each and every json file
matches_list = []

## making dataframe for each and every match and appending it to matches_list
for path in file_path_matches:
    ## loading each json file
    match_temp = json.load(open(path, 'r', encoding='utf-8'))
    
    ## flattening each json file
    match_temp_flatten = [uiv.flatten_json(x) for x in match_temp]
    
    ## making the dataframe for each json file
    matches_df = pd.DataFrame(match_temp_flatten)
    
    ## addin it to the list
    matches_list.append(matches_df)
    
## combining the dataframes present in the matches_list
all_matches_df = pd.concat(matches_list, sort='False')

## saving the dataframe as csv file
all_matches_df.to_csv('all_matches_df.csv')

## since we have a lot of null values in our dataframe so we will remove it
## and create a new dataframe and then save it as a csv file
all_matches_clean = all_matches_df.dropna(axis=1)
all_matches_clean.to_csv('all_matches_clean.csv')

## obtaining events 

## path where all matches files are stored
path = '../Statsbomb/data/events'       

## calling the function to get the list of path to all the matches json files
file_path_events = uiv.find_json(path, name='events')

path = file_path_events[0]

event_temp = json.load(open(path, 'r', encoding='utf-8'))

event_temp_flatten = [uiv.flatten_json(x) for x in event_temp]
event_df = pd.DataFrame(event_temp_flatten)

uiv.find_tactics_index(event_temp)

team_list = []

for index in range(0,2):
    team_dict = {
            'player_name': [],
            'team_name': [],
            'team_id': [],
            'formation': [],
            'jersey_num': [],
            'player_id': [],
            'player_pos': [],
            'position_id': []
            }
    
    team_name = event_temp[index]['team']['name']
    team_id = event_temp[index]['team']['id']
    formation = event_temp[index]['tactics']['formation']
    lineups = event_temp[index]['tactics']['lineup']
    
    for i in range(len(lineups)):
        jersey_num = lineups[i]['jersey_number']
        player_name = lineups[i]['player']['name']
        player_id = lineups[i]['player']['id']
        player_pos = lineups[i]['position']['name']
        pos_id = lineups[i]['position']['id']
        
        team_dict['player_name'].append(player_name)
        team_dict['team_name'].append(team_name)
        team_dict['team_id'].append(team_id)
        team_dict['formation'].append(formation)
        team_dict['jersey_num'].append(jersey_num)
        team_dict['player_id'].append(player_id)
        team_dict['player_pos'].append(player_pos)
        team_dict['position_id'].append(pos_id)
        
    team_list.append(team_dict)

pass_df = event_df.loc[event_df['type_name'] == 'Pass', :].dropna(axis=1)














