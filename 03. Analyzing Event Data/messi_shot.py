# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 19:44:31 2020

@author: anmol
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
opponent_team = 'Real Madrid'

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

make_df = df.loc[df['type_name'] == 'Shot'].set_index('index')
make_df.dropna(inplace=True, axis=1)

for row_num, make in make_df.iterrows():
    x_loc = make['location'][0]
    y_loc = make['location'][1]        
    
    if make['player_name'] == 'Lionel Andrés Messi Cuccittini':
        circleSize = np.sqrt(make['shot_statsbomb_xg']*15)
        
        if home_team == 'Barcelona':
            touch_circle = plt.Circle((x_loc, pitch_width_Y - y_loc), circleSize, color='blue')
            
            if make['shot_outcome_name'] == 'Goal':
                touch_circle.set_alpha(0.3)
        else:
            touch_circle = plt.Circle((pitch_length_X - x_loc, y_loc), circleSize, color='blue')
            
            if make['shot_outcome_name'] != 'Goal':
                touch_circle.set_alpha(0.3)
            
        ax.add_patch(touch_circle)
        
plt.text(30, 82, 'Lionel Messi\'s Shots vs Real Madrid'.format(opponent_team))
fig.set_size_inches(12, 8)
fig.savefig('Messi\'s Shots vs Real Madrid'.format(opponent_team))
plt.show()