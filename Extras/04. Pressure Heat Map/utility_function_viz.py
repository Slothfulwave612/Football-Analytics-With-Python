# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:39:19 2020

@author: slothfulwave612

Python module for visualization.

Modules Used(4):-
1. numpy -- numerical computing library.
2. matplotlib -- plotting library.
3. mlp_toolkits -- provide more functionality for plotting
4. utility_function_io -- module containing i/o functions.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import utility_function_io as ufio

def createPitch(length, width, linecolor, ax): 
    """
    Code by @JPJ_dejong
    
    creates a plot in which the 'length' is the length of the pitch (goal to goal).
    And 'width' is the width of the pitch (sideline to sideline). 
    Fill in the unity in meters or in yards.
    """
        #check boundaries again
    if length <= 95:
        return(str("Didn't you mean meters as unity?"))
        
    elif length >= 131 or width >= 101:
        return(str("Field dimensions are too big. Maximum length is 130, maximum width is 100"))
        
    #Run program if unity and boundaries are accepted
    else:
        #Pitch Outline & Centre Line
        ax.plot([0,0],[0,width], color=linecolor, zorder=2)
        ax.plot([0,length],[width,width], color=linecolor, zorder=2)
        ax.plot([length,length],[width,0], color=linecolor, zorder=2)
        ax.plot([length,0],[0,0], color=linecolor, zorder=2)
        ax.plot([length/2,length/2],[0,width], color=linecolor, zorder=2)
        
        ## the following lines of code will create 
        ## the goal-post at both side of the pitch
        ax.plot([-3,0], [(width/2)-5,(width/2)-5], color='black', zorder=2)
        ax.plot([-3,0], [(width/2)+5,(width/2)+5], color='black', zorder=2)
        ax.plot([-3,-3], [(width/2)-5,(width/2)+5], color='black', zorder=2)
        ax.plot([length+3,length+3], [(width/2)-5,(width/2)+5], color='black', zorder=2)
        ax.plot([length,length+3], [(width/2)-5,(width/2)-5], color='black', zorder=2)
        ax.plot([length,length+3], [(width/2)+5,(width/2)+5], color='black', zorder=2)
        
        #Left Penalty Area
        ax.plot([18 ,18],[(width/2 +18),(width/2-18)],color=linecolor, zorder=2)
        ax.plot([0,18],[(width/2 +18),(width/2 +18)],color=linecolor, zorder=2)
        ax.plot([18,0],[(width/2 -18),(width/2 -18)],color=linecolor, zorder=2)
        
        #Right Penalty Area
        ax.plot([(length-18),length],[(width/2 +18),(width/2 +18)],color=linecolor, zorder=2)
        ax.plot([(length-18), (length-18)],[(width/2 +18),(width/2-18)],color=linecolor, zorder=2)
        ax.plot([(length-18),length],[(width/2 -18),(width/2 -18)],color=linecolor, zorder=2)
        
        #Left 6-yard Box
        ax.plot([0,6],[(width/2+7.32/2+6),(width/2+7.32/2+6)],color=linecolor, zorder=2)
        ax.plot([6,6],[(width/2+7.32/2+6),(width/2-7.32/2-6)],color=linecolor, zorder=2)
        ax.plot([6,0],[(width/2-7.32/2-6),(width/2-7.32/2-6)],color=linecolor, zorder=2)
        
        #Right 6-yard Box
        ax.plot([length,length-6],[(width/2+7.32/2+6),(width/2+7.32/2+6)],color=linecolor, zorder=2)
        ax.plot([length-6,length-6],[(width/2+7.32/2+6),width/2-7.32/2-6],color=linecolor, zorder=2)
        ax.plot([length-6,length],[(width/2-7.32/2-6),width/2-7.32/2-6],color=linecolor, zorder=2)
        
        #Prepare Circles; 10 yards distance. penalty on 12 yards
        centreCircle = plt.Circle((length/2,width/2),10,color=linecolor,fill=False, zorder=2)
        centreSpot = plt.Circle((length/2,width/2),0.4,color=linecolor, zorder=2)
        leftPenSpot = plt.Circle((12,width/2),0.4,color=linecolor, zorder=2)
        rightPenSpot = plt.Circle((length-12,width/2),0.4,color=linecolor, zorder=2)
        
        #Draw Circles
        ax.add_patch(centreCircle)
        ax.add_patch(centreSpot)
        ax.add_patch(leftPenSpot)
        ax.add_patch(rightPenSpot)
        
        #Prepare Arcs
        leftArc = Arc((11,width/2),height=20,width=20,angle=0,theta1=312,theta2=48,color=linecolor, zorder=2)
        rightArc = Arc((length-11,width/2),height=20,width=20,angle=0,theta1=130,theta2=230,color=linecolor, zorder=2)
        
        #Draw Arcs
        ax.add_patch(leftArc)
        ax.add_patch(rightArc)
    
    #Tidy Axes
    plt.axis('off')
    
    return ax

def make_pressure_map(match_ids, team_name, season):
    '''
    Function to make a preesure map for the entire season.
    
    Argument:
    match_ids -- list, containing match ids for a particular season.
    team_name -- str, the name of the team.
    season -- str, season
    '''
    ## making a subplot
    fig, ax = plt.subplots(figsize=(15, 8))
    
    ## creating the pitch
    ax = createPitch(120, 80, 'white', ax)
    
    ## creating the pressure matrix of size (4x6)       
    pressure_matrix = np.zeros((4, 6))
    
    ## generating event data plotting and updating
    ## values in the pressure_matrix
    for match in match_ids:
        event_df = ufio.make_event_df(match)
            
        for _, row in event_df.iterrows():
            if row['type_name'] == 'Pressure' and row['team_name'] == 'Barcelona':
                loc_x = row['location'][0]
                loc_y = row['location'][1]
                
                ## plotting the pressure locations
                ax.plot(loc_x, loc_y, color='#FFFFFF', marker='.', markersize=1.34)
                
                x = 3 - (round(loc_y) // 20)
                y = round(loc_x) // 20
                
                if y == 6:
                    y = 5
                    
                if x == -1:
                    x = 0
                
                ## incrementing the pressure_matrix values
                pressure_matrix[x][y] += 1
    
    ## generating our own color palette
    color = ['#062440', '#1F4466', '#336089', '#9993A6', '#D0B6D0', '#F2718A', '#EB3A55']        
    cmap = colors.ListedColormap(color)
              
    ## plotting pressue map on the pitch as a heatmap
    plot = ax.imshow(pressure_matrix, zorder=1, aspect="auto", extent=(0,120,0,80), cmap=cmap)    
    
    ## editing the xticks and yticks
    ax.set_xticks([-10, 130]) 
    
    ## labelling the plot
    ax.text(-5, 87, team_name, fontsize=23)
    ax.text(-5, 83, 'Pressure Heat Map | La Liga {}'.format(season), fontsize=17)
    
    ## displaying the colorbar
    axins = inset_axes(ax,
                   width="5%",  # width = 5% of parent_bbox width
                   height="50%",  # height : 50%
                   loc='lower left',
                   bbox_to_anchor=(1.03, 0., 1, 1),
                   bbox_transform=ax.transAxes,
                   borderpad=0,
                   )
    fig.colorbar(plot, cax = axins)
    
    ## saving the figure
    fig.savefig('Pressure_Map_{}_{}'.format(team_name, season), dpi=100)
    
    ## closing the plot
    plt.close('all')
