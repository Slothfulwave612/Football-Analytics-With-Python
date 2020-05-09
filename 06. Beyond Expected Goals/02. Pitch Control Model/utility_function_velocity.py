# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:49:26 2020

@author: slothfulwave612
Python module for making functions to compute velocity.

Modules Used(1):
1. numpy -- numerical computing library.
"""

import numpy as np

def remove_velocity(df):
    '''
    Function to remove velocity columns(if present) from the dataframe.
    
    Argument:
    df -- dataframe object, tracking dataframe.
    
    Returns:
    df -- dataframe object, tracking dataframe.
    '''
    cols_del = ['vx', 'vy', 'speed']
    
    columns = [cols for cols in df.columns if cols.split('_')[-1] in cols_del]
    
    df.drop(columns=columns, inplace=True)
    
    return df

def cal_velocity(df, max_speed=12, window=7):
    '''
    Fucntion to calculate velocity for the tracking dataframe.
    
    Argument:
    df -- dataframe object, tracking dataframe.
    max_speed -- int, maximum speed a player can achieve(in meters/second).
    window -- int, smoothing window size in number of frames.
    
    Returns:
    df -- dataframe object, tracking dataframe.
    '''
    remove_velocity(df)
    ## removing velocity columns if present
    
    ## getting the player ids
    player_ids = np.unique([cols[:-2] for cols in df.columns if cols.split('_')[0] in ['Home', 'Away']])
        
    ## computing the difference in time for each frame
    dt = df['Time [s]'].diff()
    
    for player in player_ids:
        ## calculating velocities
        vx = df[player + '_X'].diff() / dt
        vy = df[player + '_Y'].diff() / dt
        
        ## removing outliers
        raw_speed = np.sqrt(vx**2 + vy**2)
        vx[raw_speed > max_speed] = np.nan
        vy[raw_speed > max_speed] = np.nan
        
        ## smooting the values
        ma_window = np.ones(window) / window
        vx = np.convolve(vx, v=ma_window, mode='same')
        vy = np.convolve(vy, v=ma_window, mode='same')
        
        df[player + '_vx'] = vx
        df[player + '_vy'] = vy
        df[player + '_speed'] = np.sqrt(vx**2 + vy**2)
    
    return df
