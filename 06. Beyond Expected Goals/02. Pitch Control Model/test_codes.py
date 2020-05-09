# -*- coding: utf-8 -*-
"""
Created on Sat May  9 21:57:26 2020

@author: slothfulwave612

Here we will using function from our
utility files to draw pitch maps and other
vizualizations.
"""

import utility_function_io as ufio
import utility_function_viz as ufvz
import utility_function_velocity as ufvel
import utility_function_pitch_control as ufpc

## setting path and game id
path = '../../Metrica_Sports/data'
game_id = 2

## reading in the event data
event_data = ufio.read_event_data(path, game_id)

## reading in the tracking data for both the teams
tracking_home = ufio.read_tracking_data(path, game_id, team_name='Home')
tracking_away = ufio.read_tracking_data(path, game_id, team_name='Away')

## converting coordinate values for both tracking and event dataframes
event_data = ufio.convert_values(event_data)
tracking_home = ufio.convert_values(tracking_home)
tracking_away = ufio.convert_values(tracking_away)

## reversing the direction of play
event_data, tracking_home, tracking_away = ufio.rev_direction(event_data, tracking_home, tracking_away)

## calculating players velocities
tracking_home = ufvel.cal_velocity(tracking_home)
tracking_away = ufvel.cal_velocity(tracking_away)

## making a shot and goal dataframe from event dataframe
shots_df = event_data.loc[event_data['Type'] == 'SHOT'].copy()     ## contains all the shots
goal_df = shots_df.loc[shots_df['Subtype'].str.contains('-GOAL')].copy() ## contains all the goals

## plotting the some of the passes leading to the second goal.
fig, ax = ufvz.plot_pitch()
fig, ax = ufvz.plot_events(df=event_data.loc[818: 823, :], fig=fig, ax=ax)

## getting the default model parameters
params = ufpc.default_model_params()

## generating pitch control surface for the pass in event_data at index 818
