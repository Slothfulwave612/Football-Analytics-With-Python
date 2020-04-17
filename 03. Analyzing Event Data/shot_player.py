# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 19:44:31 2020

@author: slothfulwave612

This Python module will help users to create a pitch
map for shots taken by Barcelona player that played in the 
El Clasico of 2009 where the result ended in favour
of Barcelona(2:6).

Modules Used(5):
---------------
1. matplotlib -- the vizualization library.
2. numpy -- the numerical computation library.
3. json -- module to work with JSON files.
4. pandas -- module to work with dataframes.
5. FCPython -- module to create football pitch map.
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
(fig,ax) = createPitch(pitch_length_X, pitch_width_Y,'yards','grey')

## match id for our El Clasico
match_id = 69249
home_team = 'Real Madrid'
away_team = 'Barcelona'
player_name = 'Lionel Andrés Messi Cuccittini'

## this is the name of our event data file for
## our required El Clasico
file_name = str(match_id) + '.json'

## loading the required event data file
##with open('../Statsbomb/data/events/' + file_name) as event_data:
    ##my_data = json.load(event_data, encoding='utf-8')    
my_data = json.load(open('../Statsbomb/data/events/' + file_name, 'r', encoding='utf-8'))

## get the nested structure into a dataframe 
## store the dataframe in a dictionary with the match id as key
df = json_normalize(my_data, sep='_').assign(match_id = file_name[:-5])

## making the list of all column names
column = list(df.columns)

## all the type names we have in our dataframe
all_type_name = list(df['type_name'].unique())

## creating the shots dataframe
shots_indv_df = df.loc[df['type_name'] == 'Shot'].set_index('index')
shots_indv_df.dropna(inplace=True, axis=1)
shots_indv_df = shots_indv_df.loc[shots_indv_df['player_name'] == player_name, :]

for row_num, shot in shots_indv_df.iterrows():
    x_loc = shot['location'][0]
    y_loc = shot['location'][1]        
    
    if shot['player_name'] == player_name:
        circleSize = np.sqrt(shot['shot_statsbomb_xg']*15)
        
        touch_circle = plt.Circle((pitch_length_X - x_loc, y_loc), circleSize, color='blue')
            
        if shot['shot_outcome_name'] != 'Goal':
            ## if shot outcome is not a goal then fade the circle
            touch_circle.set_alpha(0.3)
            
        ax.add_patch(touch_circle)

## placing the text on the plot        
plt.text(10, 82, '{}\'s Shots vs Real Madrid'.format(player_name), fontsize=12)
plt.text(80, 85, 'Darker Circles: Shot\'s outcome is a goal', fontsize=12)
plt.text(80, 82, 'Faded Circles: Shot\'s outcome is not a goal', fontsize=12)
    
## editing and saving the plot
fig.set_size_inches(12, 8)
fig.savefig('{}\'s Shots vs Real Madrid'.format(player_name))

## displaying the figure
plt.show()