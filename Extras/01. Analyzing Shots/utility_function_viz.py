# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:27:24 2020

@author: slothfulwave612

Python module for visualization.

Modules Used(1):-
1. matplotlib -- plotting library.
"""

import matplotlib.pyplot as plt

def create_goal_post(gray_value='#606060', fill_value='#D3D3D3', fig_size=(30, 13)):
    '''
    Function to create a goal post.
    
    Arguments:
    gray_value -- str, hex value of color, default is #606060.
    fill_value -- str, hex value for the color to be filled between the lines, default is #C0C0C0.
    back_color -- str, background color, default is whitesmoke
    fig_size -- tuple, of length and width; defining our figure size.
    
    Returns:
    fig, ax -- figure and axis objects.
    '''
    
    ## making a subplot of size fig_size
    fig, ax = plt.subplots(figsize=fig_size)
    
    ## plotting our goal post    
    ax.plot([32, 48], [0, 0], color=gray_value)
    ax.plot([36, 36], [0, 2.67], color='k')
    ax.plot([44, 44], [0, 2.67], color='k')
    ax.plot([36, 44], [2.67, 2.67], color='k')
    ax.plot([35.9, 35.9], [0, 2.75], color='k')
    ax.plot([44.1, 44.1], [0, 2.75], color='k')
    ax.plot([35.9, 44.1], [2.75, 2.75], color='k')
    
    ## filling color between the lines
    ax.fill_between([35.9, 36], [2.67, 2.67], color=fill_value)
    ax.fill_between([44.1, 44], [2.67, 2.67], color=fill_value)
    ax.fill_between(x=[35.9, 44.1], y1=[2.67, 2.67], y2=[2.75, 2.75], color=fill_value)
    
    ## plotting some inside lines of our goal post
    ax.plot([36, 36.3], [2.67, 2.58], color=gray_value)
    ax.plot([36.3, 36.7], [2.58, 0.8], color=gray_value)     
    ax.plot([36.7, 36], [0.8, 0], color=gray_value)          
    ax.plot([44, 43.7], [2.67, 2.58], color=gray_value)
    ax.plot([43.7, 43.3], [2.58, 0.8], color=gray_value)
    ax.plot([43.3, 44], [0.8, 0], color=gray_value)            
    ax.plot([36.7, 43.3], [0.8, 0.8], color=gray_value)  
            
    ## removing the ticks and the axis labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig, ax

def plot_shots(shots_df, ax):
    '''
    Function to plot the shots on the goal post figure.
    
    Arguments:
    shots_df -- dataframe object, containing shots data.
    ax -- axis object.
    
    Returns:
    ax -- axis object.
    '''
    ## traversing the dataframe
    for row_num, shot_data in shots_df.iterrows():
        shot_location = shot_data['shot_end_location']    
        shot_outcome = shot_data['shot_outcome_name']

        if shot_outcome == 'Goal':
            ## green color
            color = 'g'
            marker = '*'
        
        elif shot_outcome == 'Post':
            ## blue color
            color = 'b'
            marker = '2'
        
        elif shot_outcome == 'Off T':
            ## magenta color
            color = 'm'
            marker = 'D'
        
        elif shot_outcome == 'Saved':
            ## red color
            color = 'r'
            marker = 'X'
        
        elif shot_outcome == 'Saved to Post':
            ## red color
            color = 'r'
            marker = 'x'
        
        elif shot_outcome == 'Saved Off Target':
            ## red color
            color = 'r'
            marker = '+'
        
        ax.plot(shot_location[1], shot_location[2], color=color, label=shot_outcome, marker=marker,
                markersize=12)
        
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=20)

    return ax
