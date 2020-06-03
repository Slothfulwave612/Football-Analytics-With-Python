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
    
def plot_shot_map(shot_df, through_ids):
    '''
    Function to plot the shot map.
    
    Arguments:
    shot_df -- dataframe object, containing all shots
    '''
    fig, ax = vertical_shot_pitch(linecolor='#444444')
    ## making a pitch map    
    
    rect_x, rect_y = 10, 85
    drect_x, drect_y = 15, 85
    brect_x, brect_y = 20, 85
    
    rect = plt.Rectangle((rect_x, rect_y), 3.5, 3, fill=False)
    drect1 = plt.Rectangle((drect_x, drect_y), 3.5, 3, fill=False)
    drect2 = plt.Rectangle((drect_x + 0.35, drect_y+0.32), 2.8, 2.3, fill=False)
    brect = plt.Rectangle((brect_x, brect_y), 3.5, 3, lw=2.7, fill=False)
    
    ax.add_patch(rect)
    ax.add_patch(drect1)
    ax.add_patch(drect2)
    ax.add_patch(brect)
    
    tri_x, tri_y = 27, 86
    dtri_x, dtri_y = 32, 86
    btri_x, btri_y = 37, 86
    
    tri = Polygon([[tri_x - 1.75, tri_y - 1.75], [tri_x + 1.75, tri_y - 1.75], [tri_x, tri_y + 1.75]], fill=False)
    dtri_1 = Polygon([[dtri_x - 1.5, dtri_y - 1.5], [dtri_x + 1.5, dtri_y - 1.5], [dtri_x, dtri_y + 1.5]], fill=False)
    dtri_2 = Polygon([[dtri_x - 2.1, dtri_y - 1.8], [dtri_x + 2.1, dtri_y - 1.8], [dtri_x, dtri_y + 2.3]], fill=False)
    btri = Polygon([[btri_x - 1.75, btri_y - 1.75], [btri_x + 1.75, btri_y - 1.75], [btri_x, btri_y + 1.75]], fill=False, lw=2.7)
    
    ax.add_patch(tri)
    ax.add_patch(dtri_1)
    ax.add_patch(dtri_2)
    ax.add_patch(btri)
    
    kite_x, kite_y = 42, 86
    dkite_x, dkite_y = 47, 86
    bkite_x, bkite_y = 51, 86
    
    kite = Polygon([[kite_x - 1.75, kite_y], [kite_x, kite_y + 1.75], [kite_x + 1.75, kite_y], [kite_x, kite_y - 2]], fill=False)
    dkite_1 = Polygon([[dkite_x - 1.5, dkite_y], [dkite_x, dkite_y + 1.5], [dkite_x + 1.5, dkite_y], [dkite_x, dkite_y - 1.75]], fill=False)
    dkite_2 = Polygon([[dkite_x - 2, dkite_y], [dkite_x, dkite_y + 2], [dkite_x + 2, dkite_y], [dkite_x, dkite_y - 2.25]], fill=False)
    bkite = Polygon([[bkite_x - 1.75, bkite_y], [bkite_x, bkite_y + 1.75], [bkite_x + 1.75, bkite_y], [bkite_x, bkite_y - 2]], fill=False, lw=2.7)
    
    ax.add_patch(kite)
    ax.add_patch(dkite_1)
    ax.add_patch(dkite_2)
    ax.add_patch(bkite)
    
    fig
    
    
    
    
    
    
    
    
    
    