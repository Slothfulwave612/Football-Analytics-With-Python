# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:43:14 2020

@author: anmol
"""
import numpy as np
from os import listdir

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def fill_value(name_1, name_2):
    '''
    Function will fill the name values in required columns
    
    Arguments:
    name_1 -- str/nan, name from first column.
    name_2 -- str/nan, name from second column.
    
    Returns:
    name_1 if name_2 is nan
    name_2 if name_1 is nan
    '''
    
    if name_1 == np.nan:
        return name_2
    else:
        return name_1
    
def find_json(path, name):
    '''
    Function will find the data files in the given directory passed as
    an argument. It will list the path to all the directory and append
    it to a list and then return it.
    
    Arguments:
    path -- str, the path of the directory.
    
    Returns:
    file_path -- list, list containing the paths.
    '''
    file_path = []
    
    for folder in listdir(path):
        if name == 'matches':
            for sub_folder in listdir(path + '/' + folder):
                file_path.append(path + '/' + folder + '/' + sub_folder)
        elif name == 'events':
            file_path.append(path + '/' + folder)
    
    return file_path
            
def find_tactics_index(event_temp):
    '''
    Function to print the index value where tactic is present in the
    event data list.
    
    Argument:
    event_temp -- list, containing event data.        
    '''
    ## a counter initialized to zero
    c = 0
    
    ## iterating through the list
    for i in range(len(event_temp)):
        ## if tactic is found
        if event_temp[i].get('tactics') != None:
            print(i, end=' ')
            c += 1
            
            if c == 2:
                return
            
def make_pass_df(pass_df, id_num):
    '''
    Function will make a passing dataframe for the team.
    
    Argument:
    pass_df -- dataframe object, passing dataframe for a particular team.
    id_num -- int, the team id.
    
    Returns:
    pass_df -- dataframe object, after performating data cleaning.
    '''
    
    cols_to_select = [
            'location_0',
            'location_1',
            'possession',
            'player_id',
            'pass_height_name',
            'pass_recipient_id',
            'pass_end_location_0',
            'pass_end_location_1',
            'pass_length',
            'pass_angle',
            'pass_body_part_name'
            ]
    pass_df = pass_df.loc[:, cols_to_select]
    
    ## now since our pass_recipient_id and pass_body_part_name have some null values
    ## so filling 0 at pass_recipient_id and 'not-listed' in pass_body_part_name
    pass_df['pass_recipient_id'].fillna(0, inplace=True)
    pass_df['pass_body_part_name'].fillna('Other', inplace=True)
    
    rename_cols = {
            'possession': 'Possession',
            'player_id': 'Passer',
            'location_0': 'X_Pass',
            'location_1': 'Y_Pass',
            'pass_recipient_id': 'Receiver',
            'pass_end_location_0': 'X_Receive',
            'pass_end_location_1': 'Y_Receive',
            'pass_length': 'Pass_Length',
            'pass_angle': 'Pass_Angle',
            'pass_body_part_name': 'Body_Part',
            'pass_height_name': 'Pass_Type'
            }
    
    pass_df.rename(columns=rename_cols, inplace=True)
    
    pass_df['poss'] = pass_df.loc[:, 'Possession']
    pass_df['seq'] = pass_df.groupby('Possession')['poss'].rank(method='first')
    pass_df.drop('poss', inplace=True, axis=1)
    
    pass_df['team_id'] = id_num
    
    return pass_df
            
            
            
            
            
            
            
            
            
            
            
            
            