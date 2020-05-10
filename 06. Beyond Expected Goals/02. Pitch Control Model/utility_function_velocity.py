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


class Player:
    '''
    class defining a player object that stores position, velocity, time-to-intercept and pitch control
    contribution for a player.
    '''
    
    def __init__(self, pid, team, team_name, params):
        '''
        Function to initialize Player class objects.
        
        Arguments:
        self -- represents the object of the class.
        pid -- player id.
        team -- tracking frame.
        team_name -- 'Home' or 'Away'.
        params -- dictionary containing default parameters for pitch control model.
        '''
        self.id = pid
        self.team_name = team_name
        self.player_name = '{0}_{1}'.format(team_name, pid)
        self.v_max = params['max_player_speed']  ## maximum player speed in m/s
        self.reaction_time = params['reaction_time']
        self.sigma = params['sigma']
        self.get_position(team)
        self.get_velocity(team)
        self.PPCF = 0
    
    def get_position(self, team):
        '''
        Function to get the postion of the player.
        If the position is NaN inframe will be set to False
        
        Arguments:
        self -- represents the object of the class.
        team -- tracking frame
        '''
        self.position = np.array([team[self.player_name + 'x'], team[self.player_name + 'y']])
        self.inframe = not np.any(np.isnan(self.position))
    
    def get_velocity(self, team):
        '''
        Function to get the velocity of the player.
        If the velocity of the player is zero than set the velocity array to 0, 0 for x and y respectively.
        
        Arguments:
        self -- represents the object of the class.
        team -- tracking frame.
        '''
        self.velocity = np.array([team[self.player_name + 'vx'], team[self.player_name + 'vy']])
        if np.any(np.isnan(self.velocity)):
            self.velocity = np.array([0.0, 0.0])
        
    def time_to_intercept_fun(self, final_pos):
        '''
        Function that computes time to intercept value.
        
        Arguments:
        self -- represents the object of the class.
        final_pos -- time taken by the player to reach the final_position.
        
        ReturnsL
        time_to_intercept -- time taken to intercept the ball.
        '''
        self.PPCF = 0.0
        ## Time to intercept assumes that the player continues moving at current velocity for 'reaction_time'
        ## and then runs at full speed to the target position.
        
        reaction = self.position + self.velocity * self.reaction_time
        self.time_to_intercept = self.reaction_time + np.linalg.norm(final_pos - reaction) / self.v_max
        
        return self.time_to_intercept
    
    def probability_intercept_ball(self, arr_time):
        '''
        Function to compute the probability of a player to intercept the ball.
        
        Arguments:
        self -- represents the object of the class.
        arr_time -- time taken by the player to arrive at the target location of the ball.
        '''
        probab = 1 / (1 + np.exp(-np.pi / np.sqrt(3.0) / self.sigma * (arr_time - self.time_to_intercept)))
        
        return probab
        

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
   
def initialize_players(team, team_name, params):
    '''
    Function to create a list of players that hold their position and velocities from tracking dataframe.
    
    Arguments:
    team -- tracking_data for either home team or away team.
    team_name -- either 'Home' or 'Away'.
    params -- dict, dictionary of default parameters for our pitch control model.
    
    Returns:
    team_players -- list having player positions and velocities.
    '''
    ## getting player ids
    player_ids = np.unique([c[:-2] for c in team.columns if c.split('_')[0] in ['Home', 'Away']])
    
    ## create empty list
    team_players = []
    
    for pid in player_ids:
        team_player = Player(pid, team, team_name, params)
        if team_player.inframe:
            team_players.append(team_player)
    
    return team_players
    

def generate_pitch_control_for_events(event_id, event_data, tracking_home, tracking_away, params):
    '''
    Function for generating the pitch control surface for any given event.
    
    Arguments:
    event_id -- int, index of the event in event's dataframe.
    event_data -- event dataframe.
    tracking_home -- tracking data for home team.
    tracking_away -- tracking data for away team.
    params -- dict, default parameters for our model.
    
    Returns:
    ----
    '''
    field_dims = (105, 68)
    ## field dimension for our pitch map
    
    n_grid_cell_x = 50
    ## number of pixels in the grid(in x-direction) 
    ## n_grid_cell_y will be calculated based on n_grid_cell_x and field dimensions
    
    ## getting the starting frame, team in possession, ball's starting position
    pass_frame = event_data.loc[event_id, 'Start Frame']
    pass_team = event_data.loc[event_id, 'Team']
    ball_start_pos = np.array([event_data.loc[event_id, 'Start X'], event_data.loc[event_id, 'Start Y']])
    
    ## breaking the pitch down into grids
    n_grid_cell_y = int(n_grid_cell_x * field_dims[1]) / field_dims[0]
    x_grid = np.linspace(-field_dims[0] / 2, field_dims[0] / 2, n_grid_cell_x)
    y_grid = np.linspace(-field_dims[1] / 2, field_dims[1] / 2, n_grid_cell_y)
    
    ## initializing pitch control grids for attacking and defending teams
    PPCF_a = np.zeros(shape=(len(y_grid), len(x_grid)))
    PPCF_d = np.zeros(shape=(len(y_grid), len(x_grid)))
    
    ## initializing player positions and velocities for pitch control calculations
    if pass_team == 'Home':
        attacking_players = initialize_players(tracking_home.loc[pass_frame], 'Home', params)
        defending_players = initialize_players(tracking_away.loc[pass_frame], 'Away', params)
    elif pass_team == 'Away':
        attacking_players = initialize_players(tracking_away.loc[pass_frame], 'Away', params)
        defending_players = initialize_players(tracking_home.loc[pass_frame], 'Home', params)
    else:
        assert False, "Team in possession must be either home or away"
