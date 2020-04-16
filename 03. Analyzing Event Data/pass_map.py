# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 19:35:22 2020

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

## creating a data frame for pass
## and then removing the null values
pass_df = df.loc[df['type_name'] == 'Pass'].set_index('id')
pass_df.dropna(inplace=True, axis=1)

## iterating through the pass dataframe
for row_num, passed in pass_df.iterrows():   
    
    if passed['player_name'] == 'AndrÃ©s Iniesta LujÃ¡n':
        ## for away side
        x_loc = passed['location'][0]
        y_loc = passed['location'][1]
        
        shot_circle = plt.Circle((pitch_length_X - x_loc, y_loc), radius=2, color='blue')
        shot_circle.set_alpha(alpha=0.2)
        ax.add_patch(shot_circle)
        
        pass_x = 120 - passed['pass_end_location'][0]
        pass_y = passed['pass_end_location'][1] 
        dx = ((pitch_length_X - x_loc) - pass_x)
        dy = y_loc - pass_y
        
        pass_arrow = plt.Arrow(pitch_length_X - x_loc, y_loc, -dx, -dy, width=3)
        ax.add_patch(pass_arrow)

fig.set_size_inches(12, 8)
fig.savefig('pass_pitch_map.jpg', dpi=100)
plt.show()