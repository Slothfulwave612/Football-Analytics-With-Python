# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:31:09 2020

@author: slothfulwave612

Python file for making shot plot.

Modules Used(2):-
3. utility_function_io -- Python module for i/o operation.
4. utility_function_viz -- Python module for visualization.
"""
import utility_function_io as ufio
import utility_function_viz as ufvz

## making dataframe for competitions
comp_df = ufio.get_competitions()

## picking competition_id = 11 and season_id = 24 from comp df
## La Liga Competition, 2012-13 season
comp_id = 11
season_id = 24

## getting match dataframe from our required competiton and season
match_df = ufio.get_matches(comp_id, season_id)

## renaming the required columns
match_df_cols = list(match_df.columns)                  ## making list of the columns
match_df_cols = ufio.renaming_columns(match_df_cols)    ## new list with renamed columns
match_df.columns = match_df_cols                        ## renaming the columns

## converting match_date to datetime object
match_df = ufio.convert_to_datetime(match_df)

## the start date and end date 
start_date = '2012-11-10'
end_date = '2013-05-13'

## creating our required dataframe
scoring_df = ufio.get_selected_match(match_df, start_date, end_date)

## storing match_id for each games listed in scoring_df
scoring_df_ids = list(scoring_df['match_id'].unique())

## making the required dataframe
## for the shots taken by Messi in his 21 games
shots_df = ufio.get_selected_events(scoring_df_ids)

## plotting our goal post
fig, ax = ufvz.create_goal_post()

## plotting shots
ax = ufvz.plot_shots(shots_df, ax)

## saving figure
fig.savefig('shot_taken')
