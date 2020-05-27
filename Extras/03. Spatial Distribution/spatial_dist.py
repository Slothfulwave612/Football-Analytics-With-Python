# -*- coding: utf-8 -*-
"""
Created on Tue May 26 01:24:36 2020

@author: slothfulwave612

Thanks to soccer analytics handbook for the inspiration.

Plotting spatial distribution for Lionel Messi, Andrés Iniesta,
and Xavi Hernández.

Module Used(2):
1. utility_function_io -- for i/o operations.
2. utility_function_viz -- for visualization operations.
"""

import utility_function_io as ufio
import utility_function_viz as ufvz

## making dataframe for competitions
comp_df = ufio.get_competitions()

## La Liga Competition
comp_id = 11

## season id list
season_list = [39, 41, 22]
season_dict = {39: '2006-2007 (3-3)', 41: '2008-2009 (2-6)', 22: '2010-2011 (5-0)'}
plot_title = {39: 'La Liga 2006-2007: Barcelona vs Real Madrid (3-3)', 
              41: 'La Liga 2008-2009: Real Madrid vs Barcelona (2-6)', 
              22: 'La Liga 2010-2011: Barcelona vs Real Madrid (5-0)'}

## getting match_ids for our required season in dict format
match_ids = ufio.get_req_matches(11, list(season_dict.keys()), 'Barcelona', 'Real Madrid')

## storing events for all the matches in match_ids dict
event_dict = {}
player_dict = {5503.0:'Lionel Andrés Messi Cuccittini',  5216.0: 'Andrés Iniesta Luján', 
               20131.0: 'Xavier Hernández Creus'}

for key, value in match_ids.items():
    df = ufio.get_required_events(player_dict.values(), value)
    event_dict[key] = df

## making required matrices
x_scale = 30
y_scale = 20

x_bins, y_bins = ufio.make_lists(x_scale, y_scale)

## making cumulative_actions list 
cumulative_dict = {}

for key, value in event_dict.items():
    players = ufio.cumulative_actions(value, x_scale, y_scale, x_bins, y_bins)
    cumulative_dict[key] = players

## making NMF model
model_dict = {}
    
for key, value in cumulative_dict.items():
    model = ufio.non_neg_matrix_factorization(value)
    model_dict[key] = model

## plotting the spatial distribution
for key, value in model_dict.items():
    title_save = season_dict[key]
    title_plot = plot_title[key]
    ufvz.plot_spatial_distribution(value, x_bins, y_bins, x_scale, y_scale, title_save, title_plot, player_dict)
