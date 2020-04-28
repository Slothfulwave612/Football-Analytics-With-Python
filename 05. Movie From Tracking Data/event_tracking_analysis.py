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
3. numpy -- numerical computation library.
4. pandas -- for data manipulation and analysis
5. matplotlib -- visualization library.
"""
import utility_function_viz as ufv
import utility_function_io as ufio
import utility_function_velocity as ufvel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## setting up data path
data_dir = '../Metrica_Sports/data'
game_id = 2

## reading in the events data
event_data = ufio.read_event_data(data_dir, game_id)

## Since Metrica Sports has defined their pitch map under these coordinates
## (0,0), (0,1), (1,1), (1,0) and so the Start and End positions values are
## between 0 and 1, since we have made our pitch in metric units so we have
## to convert these position values
event_data = ufio.convert_values(event_data)

## reading in tracking data for both home and away teams
tracking_data_home = ufio.read_tracking_data(data_dir, game_id, 'Home')
tracking_data_away = ufio.read_tracking_data(data_dir, game_id, 'Away')

## convert units to metric unit
tracking_data_home = ufio.convert_values(tracking_data_home)
tracking_data_away = ufio.convert_values(tracking_data_away)

## reverse the direction of play so the home team always attack from left -> right
tracking_data_home, tracking_data_away, event_data = ufio.reverse_dir(tracking_data_home,
                                                                      tracking_data_away,
                                                                      event_data)

home_vel = ufvel.calc_player_velocities(tracking_data_home, filter='moving average')
away_vel = ufvel.calc_player_velocities(tracking_data_away, filter='moving average')

ufv.save_match_clip(home_vel[73600: 73600+500], away_vel[73600: 73600+500],
                    path='movie', fname='home_goal_2_')























