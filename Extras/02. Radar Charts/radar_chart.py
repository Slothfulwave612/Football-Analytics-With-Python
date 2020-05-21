# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:04:07 2020

@author: slothfulwave612

Here we will create radar charts for Lionel Messi, 
Neymar and Luis Suarez for 2014-15 La Liga season.

Modules Used(3):-
1. uitilty_function_io -- module for i/o operations.
2. utility_function_viz -- module for visualization operations.
3. matplotlib -- visualization library.
"""
import utility_function_io as ufio
import utility_function_viz as ufvz
import matplotlib.pyplot as plt

## making dataframe for competitions
comp_df = ufio.get_competitions()

## picking competition_id = 11 and season_id = 26 from comp df
## La Liga Competition, 2014-15 season
comp_id = 11
season_id = 26

## getting match dataframe from our required competiton and season
match_df = ufio.get_matches(comp_id, season_id)

## renaming the required columns
match_df_cols = list(match_df.columns)                  ## making list of the columns
match_df_cols = ufio.renaming_columns(match_df_cols)    ## new list with renamed columns
match_df.columns = match_df_cols                        ## renaming the columns

## storing match_id for each games listed in scoring_df
match_ids = list(match_df['match_id'].unique())

## combining all events of all matches for a particular season 
event_df = ufio.get_season_events(comp_id, match_ids)

## player names
player_1 = 'Lionel Andrés Messi Cuccittini'
player_2 = 'Neymar da Silva Santos Junior'
player_3 = 'Luis Alberto Suárez Díaz'

## minutes played
min_1 = 3347
min_2 = 2570
min_3 = 2178

## getting shots stats: non-penalty-goals, shots, shots-on-target, shooting %
leo_goals, leo_shots, leo_sot, leo_shot_per = ufio.get_shot_stats(event_df, player_1, min_1)
ney_goals, ney_shots, ney_sot, ney_shot_per = ufio.get_shot_stats(event_df, player_2, min_2)
suz_goals, suz_shots, suz_sot, suz_shot_per = ufio.get_shot_stats(event_df, player_3, min_3)

## getting pass stats: pass-percentage, assists, key-passes, through-balls
leo_pass_per, leo_assist, leo_key_pass, leo_through_ball = ufio.get_pass_stats(event_df, player_1, min_1)
ney_pass_per, ney_assist, ney_key_pass, ney_through_ball = ufio.get_pass_stats(event_df, player_2, min_2)
suz_pass_per, suz_assist, suz_key_pass, suz_through_ball = ufio.get_pass_stats(event_df, player_3, min_3)

## getting interceptions + tackles
leo_int_tackle = ufio.get_int_tackles(event_df, player_1, min_1)
ney_int_tackle = ufio.get_int_tackles(event_df, player_2, min_2)
suz_int_tackle = ufio.get_int_tackles(event_df, player_3, min_3)

## getting dispossessed count
leo_diss = ufio.dispossessed(event_df, player_1, min_1)
ney_diss = ufio.dispossessed(event_df, player_2, min_2)
suz_diss = ufio.dispossessed(event_df, player_3, min_3)

## getting successful dribbles
leo_dribble = ufio.succ_dribbles(event_df, player_1, min_1)
ney_dribble = ufio.succ_dribbles(event_df, player_2, min_2)
suz_dribble = ufio.succ_dribbles(event_df, player_3, min_3)

## calculating goal conversion rate
leo_gcr = round( (leo_goals / leo_sot) * 100, 2)
ney_gcr = round( (ney_goals / ney_sot) * 100, 2)
suz_gcr = round( (suz_goals / suz_sot) * 100, 2)

## converting goals to per 90
leo_goals = ufio.convert_to_per_90(leo_goals, min_1)
ney_goals = ufio.convert_to_per_90(ney_goals, min_2)
suz_goals = ufio.convert_to_per_90(suz_goals, min_1)

## creating radar chart
params = ['Non-Penalty Goals', 'Shots', 'Shooting %', 'Passing %', 'Assists', 'Key Passes',
          'Through Balls', 'Int + Tackles', 'Dispossessed', 'Successful Dribbles', 'Goal Conversion %']

ranges = [(0.1, 0.8), (1.7, 5.0), (27, 55), (67.5, 85), (0.08, 0.48), (1.01, 2.01),
          (0.4, 1.8), (0.7, 2.5), (3.0, 1.0), (1.0, 5.5), (20, 50)]

leo_data = [leo_goals, leo_shots, leo_shot_per, leo_pass_per, leo_assist, leo_key_pass,
            leo_through_ball, leo_int_tackle, leo_diss, leo_dribble, leo_gcr]



## first for Leo Messi






        
        