# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 19:35:22 2020

@author: slothfulwave612

This Python module will help users to create a pass
map for each Barcelona player that played in the 
El Clasico of 2009 where the result ended in favour
of Barcelona(2:6).

Modules Used(4):
---------------
1. matplotlib -- the vizualization library.
2. json -- module to work with JSON files.
3. pandas -- module to work with dataframes.
4. FCPython -- module to create football pitch map
"""
import matplotlib.pyplot as plt
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
player_name = 'Xavier Hernández Creus'

## this is the name of our event data file for
## our required El Clasico
file_name = str(match_id) + '.json'

## loading the required event data file
my_data = json.load(open('../Statsbomb/data/events/' + file_name, 'r', encoding='utf-8'))

## get the nested structure into a dataframe 
## store the dataframe in a dictionary with the match id as key
df = json_normalize(my_data, sep='_').assign(match_id = file_name[:-5])

## making the list of all column names
column = list(df.columns)

## all the type names we have in our dataframe
all_type_name = list(df['type_name'].unique())

## creating a data frame for pass
## and then removing the null values
## only listing the player_name in the dataframe
pass_df = df.loc[df['type_name'] == 'Pass', :].copy()
pass_df.dropna(inplace=True, axis=1)
pass_df = pass_df.loc[pass_df['player_name'] == player_name, :]

## creating a data frame for ball receipt
## removing all the null values
## and only listing Barcelona players in the dataframe
breceipt_df = df.loc[df['type_name'] == 'Ball Receipt*', :].copy()
breceipt_df.dropna(inplace=True, axis=1)
breceipt_df = breceipt_df.loc[breceipt_df['team_name'] == 'Barcelona', :]

pass_comp, pass_no = 0, 0
## pass_comp: completed pass
## pass_no: unsuccessful pass

## iterating through the pass dataframe
for row_num, passed in pass_df.iterrows():   
    
    if passed['player_name'] == player_name:
        ## for away side
        x_loc = passed['location'][0]
        y_loc = passed['location'][1]
        
        pass_id = passed['id']
        summed_result = sum(breceipt_df.iloc[:, 14].apply(lambda x: pass_id in x))
        
        if summed_result > 0:
            ## if pass made was successful
            color = 'blue'
            label = 'Successful'
            pass_comp += 1
        else:
            ## if pass made was unsuccessful
            color = 'red'
            label = 'Unsuccessful'
            pass_no += 1
        
        ## plotting circle at the player's position
        shot_circle = plt.Circle((pitch_length_X - x_loc, y_loc), radius=2, color=color, label=label)
        shot_circle.set_alpha(alpha=0.2)
        ax.add_patch(shot_circle)
        
        ## parameters for making the arrow
        pass_x = 120 - passed['pass_end_location'][0]
        pass_y = passed['pass_end_location'][1] 
        dx = ((pitch_length_X - x_loc) - pass_x)
        dy = y_loc - pass_y
        
        ## making an arrow to display the pass
        pass_arrow = plt.Arrow(pitch_length_X - x_loc, y_loc, -dx, -dy, width=1, color=color)
        
        ## adding arrow to the plot
        ax.add_patch(pass_arrow)

## computing pass accuracy
pass_acc = (pass_comp / (pass_comp + pass_no)) * 100
pass_acc = str(round(pass_acc, 2))

## adding text to the plot
plt.text(20, 85, '{} pass map vs Real Madrid'.format(player_name), fontsize=15)
plt.text(20, 82, 'Pass Accuracy: {}'.format(pass_acc), fontsize=15)

## handling labels
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='best', bbox_to_anchor=(0.9, 1, 0, 0), fontsize=12)

## editing the figure size and saving it
fig.set_size_inches(12, 8)
fig.savefig('{} pass map.jpg'.format(player_name), dpi=200)

## showing the plot
plt.show()
