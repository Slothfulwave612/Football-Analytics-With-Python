# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:15:42 2020

@author: slothfulwave612

Modules Used(3):
----------------
1. utility_function_viz -- Python module having plot functions.
2. utility_function_io -- Python module for loading the data sets.
3. utility_function_velocity -- Python module for velocity functions.
"""
import utility_function_io as ufio
import utility_function_viz as ufv
import utility_function_velocity as ufvel

## setting path and game id
path = '../Metrica_Sports/data'
game_id = 1

## loading in the event data
event_data = ufio.read_event_data(path, game_id)

## loading in tracking data 
tracking_home = ufio.read_tracking_data(path, game_id, team_name='Home')
tracking_away = ufio.read_tracking_data(path, game_id, team_name='Away')

## convert the values
event_data = ufio.convert_values(event_data)
tracking_home = ufio.convert_values(tracking_home)
tracking_away = ufio.convert_values(tracking_away)

## reverse the direction of the play for the second half
## so that home team aways attacks from right -> left
event_data, tracking_home, tracking_away = ufio.rev_direction(event_data, tracking_home, tracking_away)

## calculating velocities for each tracking dataframe
tracking_home = ufvel.cal_velocity(tracking_home)
tracking_away = ufvel.cal_velocity(tracking_away)

## plotting frame when the first goal was scored by the home team
fig, ax = ufv.plot_pitch()
home_team_loc = tracking_home.loc[99032]
away_team_loc = tracking_away.loc[99032]
fig, ax = ufv.plot_frame(home_team_loc, away_team_loc, fig, ax)

## creating and saving a movie for our first goal
home_team = tracking_home.loc[98298: 99032+150]
away_team = tracking_away.loc[98298: 99032+150]
ufv.save_match_clip(home_team, away_team, 'home_goal', 'movie')
