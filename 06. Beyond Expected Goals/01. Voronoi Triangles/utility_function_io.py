# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:22:33 2020

@author: slothfulwave612

This Python file contain function for input output
operation for event and tracking data.

Modules Used(2):
----------------
1. pandas -- Python library for data manipulation and analysis.
2. csv -- Python module for comma seperated file manipulation.
"""

import pandas as pd
import csv

def read_event_data(data_dir, game_id):
    '''
    Function will allow to read in the events data file.
    
    Arguments:
    data_dir -- str, the directory where the sample games are present.
    game_id -- int, the sample game id to be analyzed.
    
    Returns:
    the event data
    '''
    file_loc = '/Sample_Game_{0}/Sample_Game_{0}_RawEventsData.csv'.format(game_id)
    event_data = pd.read_csv(data_dir + file_loc)       ## reading the data
    
    return event_data

def convert_values(df):
    '''
    Converting the values to metric values.
    
    ------------ ***NOTE*** ------------
    Metrica actually define the origin at the *top*-left of the field.
    ------------ ********** ------------
    
    Argument:
    df -- dataframe object
    
    Returns:
    df -- dataframe object
    '''
    ## our field dimensions
    field_dims = (105, 68)
    
    ## making list for Start and End positions for both X and Y
    x_cols = [col for col in df.columns if col[-1] == 'X']
    y_cols = [col for col in df.columns if col[-1] == 'Y']
    
    ## here converting the units
    df[x_cols] = (df[x_cols] - 0.5) * field_dims[0]
    df[y_cols] = -1 * (df[y_cols] - 0.5) * field_dims[1]
    
    return df
    
def read_tracking_data(data_dir, game_id, team_name):
    '''
    Function to read in the tracking data.
    
    Arguments:
    data_dir -- str, the directory where the sample games are present.
    game_id -- int, the sample game id to be analyzed.
    team_name -- str, home team or away team
    
    Returns:
    the event data
    '''
    ## setting the path of our file
    file_name = 'Sample_Game_{}_RawTrackingData_{}_Team.csv'.format(game_id, team_name)
    file_loc = data_dir + '/Sample_Game_' + str(game_id) + '/' + file_name 
    
    ## creating a csv file reader
    csv_file = open(file_loc, 'r') 
    reader = csv.reader(csv_file)
    
    ## 3rd element in the first line will tell whether the 
    ## team is Home team or Away Team
    teamname = next(reader)[3]
    print('Reading content for {} team'.format(teamname))
    
    ## jersey name of each player
    jerseys = [j_name for j_name in next(reader) if j_name != '']
    columns = next(reader)
    
    ## formatting the names in the columns list
    for i, j in enumerate(jerseys):
        columns[i * 2 + 3] = '{}_{}_X'.format(team_name, j)
        columns[i * 2 + 4] = '{}_{}_Y'.format(team_name, j)
    
    ## formatting the last two values in columns
    columns[-2] = 'ball_X'
    columns[-1] = 'ball_Y'
    
    track_frame = pd.read_csv(file_loc, names=columns, index_col='Frame', skiprows=3)
    
    return track_frame
    
def rev_direction(tracking_home, tracking_away):
    '''
    Function to reverse the direction of play for the second half
    so that the home team always attacks from right -> left.
    
    Arguments:
    tracking_home -- dataframe object, tacking data for home team.
    tracking_away -- dataframe object, tracking data for away team.
    
    Returns:
    tracking_home -- dataframe object, tacking data for home team.
    tracking_away -- dataframe object, tracking data for away team.
    '''
    for data in [tracking_home, tracking_away]:
        second_half_id = data['Period'].idxmax(2)
        ## getting the starting frame of second half
        
        columns = [cols for cols in data.columns if cols[-1] in ['X', 'Y']]
        ## getting columns for x and y position of ball and players
        
        data.loc[second_half_id:, columns] *= -1
    
    return tracking_home, tracking_away
