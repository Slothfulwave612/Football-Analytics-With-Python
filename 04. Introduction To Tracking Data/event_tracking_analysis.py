# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:15:42 2020

@author: anmol

Here we will be analysing some event data
as well as tracking data and will make some
plots based on the same.

Modules Used(2):
----------------
1. utility_function_one -- Python module having plot functions.
2. utility_function_two --
"""

import utility_function_viz as ufv
import utility_function_io as ufio

## setting up data path
data_dir = '../Metrica_Sports/data'
game_id = 1

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








