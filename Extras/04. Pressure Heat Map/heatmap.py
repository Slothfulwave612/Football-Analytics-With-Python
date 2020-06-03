# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:39:19 2020

@author: slothfulwave612

Here we will create the pressure map.

Modules Used(2):-
1. utility_function_io -- module where i/o functions are defined.
2. utility_function_viz -- module where visualization functions are defined.
"""
import utility_function_io as ufio
import utility_function_viz as ufvz

## making dataframe for competitions
comp_df = ufio.get_competitions()

## La Liga Competition
comp_id = 16
season_id = 24

## getting all the matches
match_df = ufio.get_matches(comp_id, season_id)

## listing all the match ids
match_ids = list(match_df['match_id'].unique())

## making the pressure map
ufvz.make_pressure_map(match_ids, 'Bayern Munich', '2012-13', 'UEFA Champions League')
