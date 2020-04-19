# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:15:42 2020

@author: slothfulwave612

Here we will be analysing some event data
as well as tracking data and will make some
plots based on the same.

Modules Used(2):
----------------
1. utility_function_one -- Python module having plot functions.
2. utility_function_two -- Python module for loading the data sets.
"""
import utility_function_viz as ufv
import utility_function_io as ufio

## setting up data path
data_dir = '../Metrica_Sports/data'
game_id = 2

## reading in the events data
event_data = ufio.read_event_data(data_dir, game_id)

## creating lists to store column values and Type values
all_event_cols = list(event_data.columns)
all_types = list(event_data['Type'].unique())

## Since Metrica Sports has defined their pitch map under these coordinates
## (0,0), (0,1), (1,1), (1,0) and so the Start and End positions values are
## between 0 and 1, since we have made our pitch in metric units so we have
## to convert these position values
event_data = ufio.convert_values(event_data)

## creating dataframe for both home and away teams
home_team = event_data.loc[event_data['Team'] == 'Home', :]
away_team = event_data.loc[event_data['Team'] == 'Away', :]

## make a shot data frame for both home and away team
shot_home = home_team.loc[home_team['Type'] == 'SHOT', :]
shot_away = away_team.loc[away_team['Type'] == 'SHOT', :]

## listing all subtypes
all_subtypes_home = list(shot_home['Subtype'].unique())
all_subtypes_away = list(shot_away['Subtype'].unique())

## plotting the shot map for both teams
## creating our football pitch
fig, ax = ufv.plot_pitch()
## plot shots home team
fig, ax = ufv.shot_map(df=shot_home, fig=fig, ax=ax)
## plot shots away team
fig, ax = ufv.shot_map(df=shot_away, fig=fig, ax=ax)
## adding text to the plot and saving it
ax.text(-30, 39, 'Home Shots(Right) vs Away Shots(Left)', fontsize=15)
fig.savefig('shot_map.jpg')
    
## plotting the events which led to first goal for home team
## creating our football pitch
fig, ax = ufv.plot_pitch()      
## plotting event 7 events that happened before the shot to the goal
fig, ax = ufv.plot_events(df=event_data.loc[190:198, :], fig=fig, ax=ax)
## adding text to the plot and saving it
ax.text(-30, 39, 'What Happened Before Goal 1(Home Team)', fontsize=15)
fig.savefig('event_map_goal_1.jpg')

## TRACKING DATA
## reading in tracking data for both home and away teams
tracking_data_home = ufio.read_tracking_data(data_dir, game_id, 'Home')
tracking_data_away = ufio.read_tracking_data(data_dir, game_id, 'Away')

## convert units to metric unit
tracking_data_home = ufio.convert_values(tracking_data_home)
tracking_data_away = ufio.convert_values(tracking_data_away)

## plotting player's position at kickoff
fig, ax = ufv.plot_pitch()
init_frame = event_data.loc[0, 'Start Frame']
fig, ax = ufv.plot_frame(tracking_data_home.loc[init_frame], tracking_data_away.loc[init_frame], fig, ax)
ax.text(-10, 39, 'Kick Off', fontsize=15)
fig.savefig('kick_off.jpg')

## plotting player's position after home team's first goal
fig, ax = ufv.plot_pitch()
init_frame = event_data.loc[198, 'Start Frame']
event_row = event_data.loc[198, :]
fig, ax = ufv.plot_frame(tracking_data_home.loc[init_frame], tracking_data_away.loc[init_frame], fig, ax, event_row)
ax.text(-20, 39, 'Home Team\'s First Goal', fontsize=15)
fig.savefig('home_team_first_goal.jpg')

## plotting the last goal of the match
fig, ax = ufv.plot_pitch()
init_frame = event_data.loc[1723, 'Start Frame']
event_row = event_data.loc[1723, :]
fig, ax = ufv.plot_frame(tracking_data_home.loc[init_frame], tracking_data_away.loc[init_frame], fig, ax, event_row)
ax.text(-20, 39, 'Last Goal of The Match', fontsize=15)
fig.savefig('last_goal.jpg')

## plotting away team's first goal
fig, ax = ufv.plot_pitch()
init_frame = event_data.loc[823, 'Start Frame']
event_row = event_data.loc[823, :]
fig, ax = ufv.plot_frame(tracking_data_home.loc[init_frame], tracking_data_away.loc[init_frame], fig, ax, event_row)
ax.text(-20, 39, 'Away Team\'s First Goal', fontsize=15)
fig.savefig('away_team_first_goal.jpg')