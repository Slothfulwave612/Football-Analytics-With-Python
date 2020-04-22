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
                flatten(a, name + '_')
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
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            