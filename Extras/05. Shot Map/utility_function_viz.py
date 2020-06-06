# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 22:25:10 2020

@author: slothfulwave612

Python module for visualization.

Modules Used(1):-
1. matplotlib -- plotting library.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, Circle, Polygon

def vertical_shot_pitch(linecolor, fig=None, ax=None): 
    '''
    Function for plotting pitch map.
    
    Arguments:
    linecolor -- str, linecolor.
    fig, ax -- figure and axis object; default set to None.
    
    Returns:
    fig, ax -- figure and axis objects.
    '''
    if ax == None:
        fig, ax = plt.subplots(figsize=(12, 8))
    
    ## pitch outline
    ax.plot([0, 80], [120, 120], color=linecolor)
    ax.plot([0, 0], [120, 80], color=linecolor)
    ax.plot([80, 80], [80, 120], color=linecolor)
    
    ## penalty box
    ax.plot([18, 18], [120, 102], color=linecolor)
    ax.plot([62, 62], [120, 102], color=linecolor)
    ax.plot([18, 62], [102, 102], color=linecolor)
    
    ## six yard box
    ax.plot([30, 30], [120, 114], color=linecolor)
    ax.plot([50, 50], [120, 114], color=linecolor)
    ax.plot([30, 50], [114, 114], color=linecolor)
    
    ## penalty box circle
    ax.plot(40, 108, marker='o', markersize=6, color=linecolor)
    
    ## penalty box arc
    arc = Arc((40,102),height=9.15,width=15,angle=0,theta1=180, theta2=0.5, color=linecolor)
    ax.add_patch(arc)
    
    #Tidy Axes
    plt.axis('off')
    
    return fig, ax    
    
    
    
    
    
    
    
    
    
