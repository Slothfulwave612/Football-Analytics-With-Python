# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:49:26 2020

@author: anmol
"""

import numpy as np
from scipy import signal

def remove_velocity(team):
    '''
    Function to remove velocity columns from the dataframe.
    
    Argument:
    team -- dataframe object, tracking data for a particular team.
    
    Returns:
    team -- dataframe object, dataframe after removing the velocity columns(if present).
    '''
    velocity_cols = ['vx', 'vy', 'ax', 'ay', 'speed', 'acceleration']
    columns = [cols for cols in team.columns if cols.split('_')[-1].lower() in velocity_cols]
    team = team.drop(columns=columns)
    
    return team

def calc_player_velocities(team, filter='Savitzky-Golay', window = 7, polyorder = 1, maxspeed = 12):
    '''
    Function to calculate velocities in x and y direction and 
    the total player speed at every timestamp.
    
    Argument:
    team -- dataframe object, tracking data for a team.
    filter -- smoothing technique.
    window -- smoothing window size in # of frames.
    polyorder -- order of polynomial for the 'Savitzky-Golay' filter
                 default is 1 - a linear fit to the velocity, so the gradient is acceleration.
    maxspeed -- the maximum speed that a player can realisitically achieve(in meters/second)
                speed measures that exceeds maxspeed are tagged as outliers and set to NaN.

    Returns:
    team -- dataframe object, the tracking DataFrame with columns for 
            speed in the x & y direction and total speed added.
    '''
    
    ## removing velocities that are already in the dataframe
    team = remove_velocity(team)
    
    ## getting player ids
    player_ids = np.unique([c[:-2] for c in team.columns if c[:4] in ['Home', 'Away']])
    
    ## caluculate the time difference, should always be 0.04s
    dt = team['Time [s]'].diff()
    
    ## index for the first frame in the second half
    second_half_idx = team['Period'].idxmax(2)
    
    ## estamiting the velocities for players in the team
    for player in player_ids:
        ##  calculating unsmoothed estimates of velocity
        vx = team[player + '_X'].diff() / dt
        vy = team[player + '_Y'].diff() / dt
        
        ## remove unsmoothed data points that exceeds the maximum speed
        raw_speed = np.sqrt(vx**2 + vy**2)      ## magnitude of the vector
        vx[raw_speed > maxspeed] = np.nan
        vy[raw_speed > maxspeed] = np.nan
        
        if filter == 'Savitzky-Golay':
            ## calculating the first half velocities
            vx.loc[:second_half_idx] = signal.savgol_filter(vx.loc[:second_half_idx], window_length=window, polyorder=polyorder)
            vy.loc[:second_half_idx] = signal.savgol_filter(vy.loc[:second_half_idx], window_length=window, polyorder=polyorder)
            
            ## calculating the second half velocities
            vx.loc[second_half_idx:] = signal.savgol_filter(vx.loc[second_half_idx:], window_length=window, polyorder=polyorder)
            vy.loc[second_half_idx:] = signal.savgol_filter(vy.loc[second_half_idx:], window_length=window, polyorder=polyorder)
        
        elif filter == 'moving average':
            ma_window = np.ones(window) / window
            
            # calculate first half velocity
            vx.loc[:second_half_idx] = np.convolve( vx.loc[:second_half_idx] , ma_window, mode='same' ) 
            vy.loc[:second_half_idx] = np.convolve( vy.loc[:second_half_idx] , ma_window, mode='same' )      
            
            # calculate second half velocity
            vx.loc[second_half_idx:] = np.convolve( vx.loc[second_half_idx:] , ma_window, mode='same' ) 
            vy.loc[second_half_idx:] = np.convolve( vy.loc[second_half_idx:] , ma_window, mode='same' )
        
        team[player + '_vx'] = vx
        team[player + '_vy'] = vy
        team[player + '_speed'] = np.sqrt(vx**2 + vy**2)
    
    return team
            
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    