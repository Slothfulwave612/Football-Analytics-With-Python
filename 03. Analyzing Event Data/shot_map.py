# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 22:51:52 2020

@author: slothfulwave612

This Python module will create a shot map for
the match between Real Madrid and Barcelona for 
the La Liga season 2008-09 which ended with the
result 2:6 in favour of Barcelona.

Then through the vizualization we will try to 
analyze the xG for each shot taken by the both 
team.

Modules Used(5):
---------------
1. matplotlib -- the vizualization library.
2. numpy -- the numerical computation library.
3. json -- module to work with JSON files.
4. pandas -- module to work with dataframes.
5. FCPython -- module to create football pitch map
"""
import matplotlib.pyplot as plt
import numpy as np
import json
from pandas.io.json import json_normalize
from FCPython import createPitch

## Note Statsbomb data uses yards for their pitch dimensions
pitch_length_X = 120
pitch_width_Y = 80

## calling the function to create a pitch map
## yards is the unit for measurement and
## gray will be the line color of the pitch map
(fig,ax) = createPitch(pitch_length_X, pitch_width_Y,'yards','gray')

## match id for our El Clasico
match_id = 69249
home_team = 'Real Madrid'
away_team = 'Barcelona'

## this is the name of our event data file for
## our required El Clasico
file_name = str(match_id) + '.json'

## loading the required event data file
with open('../Statsbomb/data/events/' + file_name) as event_data:
    clasico_data = json.load(event_data)    

## get the nested structure into a dataframe 
## store the dataframe in a dictionary with the match id as key
df = json_normalize(clasico_data, sep='_').assign(match_id = file_name[:-5])

## making the list of all column names
column = list(df.columns)

## all the type names we have in our dataframe
all_type_name = list(df['type_name'].unique())

## picking shots from all_type_name
## a dataframe of shots
shots_df = df.loc[df['type_name'] == 'Shot'].set_index('id')

## removing the columns having NaN values.
## after this we will have a pure shots dataframe
shots_df.dropna(inplace=True, axis=1)

## plotting the shots by each team
for row_num, shot in shots_df.iterrows():
    x_loc = shot['location'][0]     ## shot location x-axis
    y_loc = shot['location'][1]     ## shot location y-axis
    
    goal = shot['shot_outcome_name'] == 'Goal'
    team_name = shot['team_name']
    
    ## assigning the circleSize as per xG value
    circleSize = np.sqrt(shot['shot_statsbomb_xg']*5)
    
    if team_name == home_team:
        if goal:
            shot_circle = plt.Circle((x_loc, pitch_width_Y - y_loc), circleSize, color='red')
            player_name = ' '.join(shot['player_name'].split(' ')[:2])
            plt.text(x_loc + 2, pitch_width_Y - y_loc, player_name)
        else:
            shot_circle = plt.Circle((x_loc, pitch_width_Y - y_loc), circleSize, color='red')
            shot_circle.set_alpha(alpha=0.2)
            
    elif team_name == away_team:
        if goal:
            shot_circle = plt.Circle((pitch_length_X - x_loc, y_loc), circleSize, color='blue')
            player_name = ' '.join(shot['player_name'].split(' ')[:2])
            if player_name == 'Lionel AndrÃ©s':
                player_name = 'Messi'
            plt.text(pitch_length_X - x_loc + 2, y_loc - 1, player_name)
        else:
            shot_circle = plt.Circle((pitch_length_X - x_loc, y_loc), circleSize, color='blue')
            shot_circle.set_alpha(alpha=0.2)
    
    ax.add_patch(shot_circle)

plt.text(5,75,away_team + ' shots') 
plt.text(80,75,home_team + ' shots') 
     
fig.set_size_inches(10, 7)
fig.savefig('shots_pitch_map.jpg', dpi=100)
plt.show()

