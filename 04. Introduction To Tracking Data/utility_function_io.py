# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:22:33 2020

@author: anmol

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

def convert_values(event_data):
    '''
    Converting the values to metric values.
    
    ------------ ***NOTE*** ------------
    Metrica actually define the origin at the *top*-left of the field.
    ------------ ********** ------------
    
    Argument:
    event_data -- dataframe object, our event data frame.
    
    Returns:
    event_data -- dataframe object, our event data frame with changes Start and End
                  position values.
    '''
    ## our field dimensions
    field_dims = (105, 68)
    
    ## making list for Start and End positions for both X and Y
    x_cols = [col for col in event_data.columns if col[-1] == 'X']
    y_cols = [col for col in event_data.columns if col[-1] == 'Y']
    
    ## here converting the units
    event_data[x_cols] = (event_data[x_cols] - 0.5) * field_dims[0]
    event_data[y_cols] = -1 * (event_data[y_cols] - 0.5) * field_dims[1]
    
    return event_data
    
    
    
    
    
    
    
    
    
    