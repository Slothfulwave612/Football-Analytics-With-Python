# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:04:07 2020

@author: slothfulwave612

Here we will create radar charts for Lionel Messi, 
Neymar and Luis Suarez for 2014-15 La Liga season.

Modules Used(2):-
1. uitilty_function_io -- module for i/o operations.
2. utility_function_viz -- module for visualization operations.
"""
import utility_function_io as ufio
import utility_function_viz as ufvz

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

## labels, and ranges
labels = ['Non-Penalty Goals', 'Shots', 'Shooting %', 'Passing %', 'Assists', 'Key Passes',
              'Through Balls', 'Successful Dribbles', 'Goal Conversion %']
    
ranges = [(0.5, 1.03), (0.5, 5.5), (10, 55), (1, 85), (0.1, 0.7), (0.5, 3), 
                (0.5, 6), (0.7, 10), (20, 70)]
        ## note for different stats you have to chage the range values
   
## stats 
leo_stats = [leo_goals, leo_shots, leo_shot_per, leo_pass_per, leo_assist, leo_key_pass,
             leo_through_ball, leo_dribble, leo_gcr]

ney_stats = [ney_goals, ney_shots, ney_shot_per, ney_pass_per, ney_assist, ney_key_pass,
             ney_through_ball, ney_dribble, ney_gcr]

suz_stats = [suz_goals, suz_shots, suz_shot_per, suz_pass_per, suz_assist, suz_key_pass,
             suz_through_ball, suz_dribble, suz_gcr]

## plotting radar charts
ufvz.plot_player_data(labels, ranges, leo_stats, title='Lionel Messi: La Liga: 2014-15', save_title='leo')
ufvz.plot_player_data(labels, ranges, ney_stats, title='Neymar: La Liga: 2014-15', save_title='ney')
ufvz.plot_player_data(labels, ranges, suz_stats, title='Luis Suarez: La Liga: 2014-15', save_title='suz')
