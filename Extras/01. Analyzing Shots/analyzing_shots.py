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
import utility_function_io as ufio

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
start_date = '2012-11-11'
end_date = '2013-05-13'

## creating our required dataframe
scoring_df = ufio.get_selected_match(match_df, start_date, end_date)

## storing match_id for each games listed in scoring_df
scoring_df_ids = list(scoring_df['match_id'].unique())

## making the required dataframe
## for the shots taken by Messi in his 21 games
shots_df = ufio.get_selected_events(scoring_df_ids)
