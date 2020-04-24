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
3. seaborn -- data vizualization library.
4. utility_io_viz -- module having utility functions.
"""
import json 
import pandas as pd
import seaborn as sns
import matplotlib.style as style 
import utility_io_viz as uiv

style.use('ggplot')

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
## renaming to be done

## since we have a lot of null values in our dataframe so we will remove it
## and create a new dataframe and then save it as a csv file
all_matches_clean = all_matches_df.dropna(axis=1)

rename_list = {
        'away_team_away_team_gender' : 'away_team_gender',
        'away_team_away_team_id': 'away_team_id',
        'away_team_away_team_name': 'away_team_name',
        'competition_competition_id': 'competition_id',
        'competition_competition_name': 'competition_name',
        'home_team_home_team_gender': 'home_team_gender',
        'home_team_home_team_id': 'home_team_id',
        'home_team_home_team_name': 'home_team_name',
        'season_season_id': 'season_id', 
        'season_season_name': 'season_name'
        }

all_matches_clean.rename(columns=rename_list, inplace=True)

## obtaining events 

## path where all matches files are stored
path = '../Statsbomb/data/events'       

## calling the function to get the list of path to all the matches json files
file_path_events = uiv.find_json(path, name='events')

event_dict = {}

for path in file_path_events:
    event_temp = json.load(open(path, 'r', encoding='utf-8'))
    
    event_temp_flatten = [uiv.flatten_json(x) for x in event_temp]
    
    event_df = pd.DataFrame(event_temp_flatten)
    
    ## uiv.find_tactics_index(event_temp)
    
    starting_xi = []
    id_list = []
    
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
            
        starting_xi.append(team_dict)
        id_list.append(team_id)
    
    pass_df1 = event_df.loc[(event_df['type_name'] == 'Pass') & (event_df['team_id'] == id_list[0]), :]
    pass_df2 = event_df.loc[(event_df['type_name'] == 'Pass') & (event_df['team_id'] == id_list[1]), :]
    
    pass_df1 = uiv.make_pass_df(pass_df1, id_list[0])
    pass_df2 = uiv.make_pass_df(pass_df2, id_list[1])
    
    match_id = path.split('/')[-1].split('.')[0]
    
    pass_list = [pass_df1, pass_df2]
    
    event_dict[match_id] = [starting_xi, pass_list]

all_event_df = pd.Series(event_dict)
## squad rotation per match 
## FA Women's Super League competition_id = 37 and season_id 4
    
women_fa = all_matches_clean.loc[(all_matches_clean['competition_id'] == 37) & 
                                  (all_matches_clean['season_id'] == 4), :]

women_fa_teams = list(women_fa['home_team_name'].unique())

squad_rotation = {}
team_starting_xi = {}

for team in women_fa_teams:  
    team_starting_xi[team] = {}
    
    team_matches = women_fa.loc[(women_fa['away_team_name'] == team) | 
                                (women_fa['home_team_name'] == team), :].copy()
    
    team_matches['GD'] = team_matches.loc[:, 'home_score'] - team_matches.loc[:, 'away_score']
    
    team_events = {}
    
    for ids in team_matches['match_id'].unique():
        team_events[ids] = event_dict[str(ids)]
    
    team_id = women_fa.loc[women_fa['home_team_name'] == team, 'home_team_id'].iloc[0]
    
    team_matches['Team_GD'] = team_matches.apply(lambda x: x['GD'] if x['home_team_id'] == team_id else -x['GD'], axis=1) 
    team_matches['Result'] = team_matches['Team_GD'].apply(uiv.fill_result)
    
    ## nested loop here
    for i in team_events:
        start_xi = team_events[i][0]
        
        for index in range(len(start_xi)):
            if start_xi[index]['team_id'][0] == team_id:
                break
        
        team_11 = start_xi[index]
        team_starting_xi[team][i] = team_11['player_name']
    
    num_matches = len(team_events)
    
    sqd_rotate = {}
    
    count = 0
    prev_id = 0
    
    for i in sorted(team_starting_xi[team]):
        if count == 0:
            sqd_rotate[i] = 0
            
        count += 1
        
        if count == 2:
            length = len(set(team_starting_xi[team][prev_id]) - set(team_starting_xi[team][i]))
            sqd_rotate[i] = length
            count = 1
        
        prev_id = i
    
    team_matches['Rotated'] = team_matches['match_id'].map(sqd_rotate)
    squad_rotation[team] = team_matches.loc[:, ['match_week', 'Result', 'Rotated']]

team = 'Reading WFC'
sns.barplot(data=squad_rotation[team], x='match_week', y='Rotated', hue='Result')



