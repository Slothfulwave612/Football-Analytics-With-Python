# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:31:09 2020

@author: slothfulwave612

Modules Used(4):-
1. numpy -- numerical computing library.
2. matplotlib -- plotting library for the Python.
3. utility_function_io -- Python module for i/o operation.
4. utility_function_viz -- Python module for visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import utility_function_io as ufio
import utility_function_viz as ufvz

## making dataframe for competitions
comp_df = ufio.get_competitions()

## picking competition_id = 11 and season_id = 22 from comp df
## La Liga Competition, 2010-11 season
comp_id = 11
season_id = 22

## getting match dataframe from our required competiton and season
match_df = ufio.get_matches(comp_id, season_id)

## renaming the required columns
match_df_cols = list(match_df.columns)                  ## making list of the columns
match_df_cols = ufio.renaming_columns(match_df_cols)    ## new list with renamed columns
match_df.columns = match_df_cols                        ## renaming the columns

## getting required match id
match_id = ufio.getting_match_id(match_df, 'Barcelona', 'Real Madrid')

## making event dataframe for the particular match
events, lineups = ufio.make_event_df(match_id)

## getting our home team players
home_lineup = lineups[0]
players = ufio.get_straters(home_lineup)

## getting event values for Barcelona
team_id = home_lineup['team']['id']
event_barca = [e for e in events if e['team']['id'] == team_id]

## getting the pass events for Barcelona
pass_barca = [e for e in event_barca if e['type']['name'] == 'Pass']

## generating passing matrix
pass_matrix = ufio.passing_matrix(pass_barca)

## generating average player location
avg_location = ufio.get_avg_player_pos(event_barca, players)

## generating volumes of passes exchanged between player
lines, weights = ufio.vol_passes_exchanged(pass_matrix, players, avg_location)

## creating a pitchmap
fig, ax = plt.subplots(figsize=(20, 12))
fig, ax = ufvz.createPitch(120, 80, 'yards', 'gray', fig, ax)

## defining lambda functions
fill_adj = lambda x: 0.8 / (1 + np.exp(-(x-20)*0.2))
weight_adj = lambda x: 2 / (1 + np.exp(-(x-10)*0.2))

## creating lines for passes
ax = ufvz.show_lines(ax, lines, weights, weight_adj, fill_adj)

## drawing each player's position
ax = ufvz.draw_points(ax, [xy for k, xy in avg_location.items()])

## assigning jersey numbers to each player position
ax = ufvz.draw_numbers(ax, avg_location, players)

## setting labels
ax = ufvz.label_players(ax)

## saving the figure
fig.savefig('Passing Network.jpg')
