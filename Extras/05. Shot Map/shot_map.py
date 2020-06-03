# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 22:25:10 2020

@author: sothfulwave612

Modules Used(2):-
1. utility_function_io -- module where i/o functions are defined.
2. utility_function_viz -- module where visualization functions are defined.
"""
import utility_function_io as ufio
import utility_function_viz as ufvz

## making dataframe for competitions
comp_df = ufio.get_competitions()

## La Liga Competition
comp_id = 11
season_id = 23

## getting all the matches
match_df = ufio.get_matches(comp_id, season_id)

## listing all the match ids
match_ids = list(match_df['match_id'].unique())

## event dataframe for the whole season
team = 'Barcelona'
event_df = ufio.full_season_events(match_ids, team)

## making shot dataframe for a particular player
player_name = 'Lionel Andrés Messi Cuccittini'
shot_df = event_df.loc[
                        (event_df['player_name'] == player_name) &
                        (event_df['type_name'] == 'Shot')
                      ]

## getting through ball pass ids from event dataframe
through_ids = ufio.get_through_balls_id(event_df)

f = shot_df.loc[]