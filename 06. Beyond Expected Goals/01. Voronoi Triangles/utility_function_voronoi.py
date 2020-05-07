# -*- coding: utf-8 -*-
"""
Created on Thu May  7 20:31:08 2020

@author: slothfulwave612

This Python module will help create voronoi plots
and a match clip having voronoi triangles.

Modules Used(6):
1. os -- for interacting with the operating system.
2. numpy -- numerical computing library.
3. pandas -- for data manipulation and analysis.
4. matplotlib -- plotting library in Python.
5. scipy -- a scientific library for Python.
6. utility_function_viz -- contains function for various vizualization.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import utility_function_viz as ufv


def make_voronoi_plot(home_team, away_team, velocity=False):
    '''
    Function to make a voronoi plot for tracking data at
    a particular frame.
    
    Arguments:
    home_team -- home_team tracking points for a particular frame
    away_team -- away_team tracking points for a particular frame
    velocity -- True, for including the velocities
                False, for not including it
                
    Returns:
    fig and ax -- figure and axis object.
    '''
    ## getting each players coordinate positions
    x_coordinate, y_coordinate = [], []
    
    ## adding coordinates for home team players
    x_coordinate += list(home_team[2:24])[::2]
    y_coordinate += list(home_team[2:24])[1::2]
    
    ## adding coordinates for away team players
    x_coordinate += list(away_team[2:24])[::2]
    y_coordinate += list(away_team[2:24])[1::2]
    
    ## adding some extra coordinates
    ## because on removing them and then running the program
    ## you will see that the area around goalkeepers are not filling up
    x_coordinate.append(100)
    x_coordinate.append(100)
    x_coordinate.append(-100)
    x_coordinate.append(-100)
    y_coordinate.append(100)
    y_coordinate.append(-100)
    y_coordinate.append(100)
    y_coordinate.append(-100)
    
    ## stacking all the coordinates
    point_stack = np.vstack(([x_coordinate], [y_coordinate])).T
    
    ## creating a pitch
    fig, ax = ufv.plot_pitch()
    
    # plotting players positions
    fig, ax = ufv.plot_frame(home_team, away_team, fig, ax, velocity=velocity)
    
    ## making a list of colors for home team('red') and away team('blue')
    colors = ['red'] * 11 + ['blue'] * 11
    
    ## creating voronoi triangles
    vor = Voronoi(point_stack)    
    
    ## making a dataframe of colors and their corresponding regions
    df = pd.DataFrame(colors)
    df['region'] = vor.point_region[:-4]    ## not taking last four values
    
    ## plotting our voronoi plot
    fig = voronoi_plot_2d(vor ,show_points=False, show_vertices=False, line_colors='black',
                          line_width=2, line_alpha=0.6, point_size=2, ax=ax)
    
    ## coloring each region
    for index, region in enumerate(vor.regions):
        if not -1 in region:
            if index != 0:
                color = df.loc[df['region'] == index, 0].values[0]
                polygon =[vor.vertices[i] for i in region]
                ax.fill(*zip(*polygon), c=color, alpha=0.3)
    
    ## setting the axis values
    ax.set_xlim(-54,54)
    ax.set_ylim(-35, 35)
    
    return fig, ax

def make_voronoi_movie(home_team, away_team, events, velocity=False):
    '''
    Function to create and save a match clip.
    
    Arguments:
    home_team -- dataframe object, tracking data for home team.
    away_team -- dataframe object, tracking data for away team.
    events -- list, list of frames.
    
    velocity -- True, for including the velocities.
                False, for not including it.
    '''    
    print('Generating Movie...', end=' ')
    
    for y in events:
        ## creating pitch
        fig, ax = ufv.plot_pitch()
        
        ## generating voronoi plots
        fig, ax = make_voronoi_plot(home_team.loc[y], away_team.loc[y], velocity=velocity)
    
        ## saving generated voronoi plots
        fig.savefig('movie/Voronoi_Triangle_with_color_{}.jpg'.format(y))
        plt.close('all')
    
    ## running ffmpeg command for making videos from the plots
    os.chdir('movie')
    command = 'ffmpeg -start_number {} -i Voronoi_Triangle_with_color_%05d.jpg Voronoi_with_color.mp4'.format(events[0])
    os.system('cmd /c "{}"'.format(command))
    
    test = os.listdir()

    ## deleting all the jpg files.
    for item in test:
        if item.endswith(".jpg"):
            os.remove(item)
            
    print('Done!!!')
