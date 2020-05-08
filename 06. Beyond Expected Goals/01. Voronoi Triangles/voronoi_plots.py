# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:28:29 2020

@author: slothfulwave612

Here we will create voronoi plots based on the 
tracking data.

Modules Used(4):
1. utility_function_viz -- Python module having plot functions.
2. utility_function_io -- Python module for loading the data sets.
3. utility_function_velocity -- Python module for velocity functions.
4. utility_function_voronoi -- Python module for voronoi plot functions.
"""
import utility_function_viz as ufv
import utility_function_io as ufio
import utility_function_velocity as ufvel
import utility_function_voronoi as ufvr

## setting path and game id
path = '../Metrica_Sports/data'
game_id = 2

## loading in the tracking data
tracking_home = ufio.read_tracking_data(path, game_id, team_name='Home')
tracking_away = ufio.read_tracking_data(path, game_id, team_name='Away')

## converting values
tracking_home = ufio.convert_values(tracking_home)
tracking_away = ufio.convert_values(tracking_away)

## reversing second half direction
tracking_home, tracking_away = ufio.rev_direction(tracking_home, tracking_away)

## computing velocity
tracking_home = ufvel.cal_velocity(tracking_home)
tracking_away = ufvel.cal_velocity(tracking_away)

## plotting voronoi triangles
fig, ax = ufv.plot_pitch()
fig, ax = ufvr.make_voronoi_plot(tracking_home.loc[53027], tracking_away.loc[53027], velocity=True)
fig.savefig('voronoi_plot.jpg')

## home and away team frames
home_team = tracking_home.loc[3069: 4419+30]
away_team = tracking_away.loc[3069: 4419+30]
events = range(3069, 4419+30)

## make Delaunay Triangles
ufvr.make_movie(home_team, away_team, events=events, fname='goal_movie', team='home', velocity=True)

## making match clip: contains voronoi triangles
ufvr.make_voronoi_movie(home_team, away_team, events=events, velocity=True)
