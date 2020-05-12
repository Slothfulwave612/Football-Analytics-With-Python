"""
Created on Tue May 12 20:31:09 2020

@author: anmol
"""
import utility_function_io as ufio
import utility_function_viz as ufv

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
event_df = ufio.make_event_df(match_id)

## loading up the lineups for the match
