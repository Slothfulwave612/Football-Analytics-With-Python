# -*- coding: utf-8 -*-
"""
Created on Sat May  9 22:00:35 2020

@author: slothfulwave612

This Python module will contain all the required
function for making a pitch control model.

This code was contributed on Friend of Tracking by Laurie Shaw
and the pitch control model concepts are from William Spearman's
research paper 'Beyond Expected Goals'

I have made notes on same on my GitHub Repository, more further explanation 
of the model you can check it out.
"""

import numpy as np

def default_model_params(time_to_control = 3):
    '''
    Function contains all the parameters and their default 
    values so that we can use it for our pitch control 
    model building.
    
    Argument:
    time_to_control -- int, it is the minimum time a used by the player to control the ball
                       represented as 10^time_to_control.
                       If any player has less than 10^time_to_control value we will see it as
                       an outlier and will ignore that player.
                       
    Returns:
    params: dict, parameters required to build the model.
    '''
    params = {}
    ## dictionary will contain all the required parameters
    
    ## model parameters
    
    params['max_player_acc'] = 7.0 
    ## maximum player acceleration = 7.0 m/s^2
    
    params['max_player_speed'] = 5.0 
    ## maximum player speed = 5.0 m/s
    
    params['reaction_time'] = 0.7
    ## time take by the player to react and change trajectory = 0.7 second
    
    params['sigma'] = 0.45
    ## standard deviation of sigmoid function in Spearman's model
    ## determines uncertainity in player's arrival time
    
    params['kappa_def'] = 1.72
    ## kappa parameter defined in Spearman's model
    ## gives advantage to defending players to control the ball
    
    params['lambda_att'] = 4.3
    ## ball control parameter for attacking team
    
    params['lambda_def'] = 4.3 * params['kappa_def']
    ## ball control parameter for defending team
    
    params['avg_ball_speed'] = 15
    ## average ball speed = 15 m/s
    
    params['int_dt'] = 0.04
    ## integration timestep(dt)
    
    params['max_int_time'] = 10
    ## upper limit on integral time
    
    params['model_converge_tol'] = 0.01
    ## assume convergence when PPCF>0.99 at a given location.
    ## The following are 'short-cut' parameters. We do not need to calculated PPCF 
    ## explicitly when a player has a sufficient head start. 
    ## A sufficient head start is when the a player arrives at the target location 
    ## at least 'time_to_control' seconds before the next player
    
    params['time_to_control_att'] = time_to_control * np.log(10) * (np.sqrt(3) * params['sigma'] / np.pi + 1/params['lambda_att'])
    params['time_to_control_def'] = time_to_control * np.log(10) * (np.sqrt(3) * params['sigma'] / np.pi + 1/params['lambda_def'])
    
    return params
