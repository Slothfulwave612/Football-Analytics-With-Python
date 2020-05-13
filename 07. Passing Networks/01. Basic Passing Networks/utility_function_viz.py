# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:27:24 2020

@author: slothfulwave612

Python module for visualization.

Modules Used(1):-
1. matplotlib -- plotting library.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import matplotlib.patches as patches

def createPitch(length,width, unity,linecolor, fig, ax): # in meters
    # Code by @JPJ_dejong

    """
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
        ax.plot([0,0],[0,width], color=linecolor)
        ax.plot([0,length],[width,width], color=linecolor)
        ax.plot([length,length],[width,0], color=linecolor)
        ax.plot([length,0],[0,0], color=linecolor)
        ax.plot([length/2,length/2],[0,width], color=linecolor)
        
        ## the following lines of code will create 
        ## the goal-post at both side of the pitch
        ax.plot([-3,0], [(width/2)-5,(width/2)-5], color=linecolor)
        ax.plot([-3,0], [(width/2)+5,(width/2)+5], color=linecolor)
        ax.plot([-3,-3], [(width/2)-5,(width/2)+5], color=linecolor)
        ax.plot([length+3,length+3], [(width/2)-5,(width/2)+5], color=linecolor)
        ax.plot([length,length+3], [(width/2)-5,(width/2)-5], color=linecolor)
        ax.plot([length,length+3], [(width/2)+5,(width/2)+5], color=linecolor)
        
        #Left Penalty Area
        ax.plot([18 ,18],[(width/2 +18),(width/2-18)],color=linecolor)
        ax.plot([0,18],[(width/2 +18),(width/2 +18)],color=linecolor)
        ax.plot([18,0],[(width/2 -18),(width/2 -18)],color=linecolor)
        
        #Right Penalty Area
        ax.plot([(length-18),length],[(width/2 +18),(width/2 +18)],color=linecolor)
        ax.plot([(length-18), (length-18)],[(width/2 +18),(width/2-18)],color=linecolor)
        ax.plot([(length-18),length],[(width/2 -18),(width/2 -18)],color=linecolor)
        
        #Left 6-yard Box
        ax.plot([0,6],[(width/2+7.32/2+6),(width/2+7.32/2+6)],color=linecolor)
        ax.plot([6,6],[(width/2+7.32/2+6),(width/2-7.32/2-6)],color=linecolor)
        ax.plot([6,0],[(width/2-7.32/2-6),(width/2-7.32/2-6)],color=linecolor)
        
        #Right 6-yard Box
        ax.plot([length,length-6],[(width/2+7.32/2+6),(width/2+7.32/2+6)],color=linecolor)
        ax.plot([length-6,length-6],[(width/2+7.32/2+6),width/2-7.32/2-6],color=linecolor)
        ax.plot([length-6,length],[(width/2-7.32/2-6),width/2-7.32/2-6],color=linecolor)
        
        #Prepare Circles; 10 yards distance. penalty on 12 yards
        centreCircle = plt.Circle((length/2,width/2),10,color=linecolor,fill=False)
        centreSpot = plt.Circle((length/2,width/2),0.8,color=linecolor)
        leftPenSpot = plt.Circle((12,width/2),0.8,color=linecolor)
        rightPenSpot = plt.Circle((length-12,width/2),0.8,color=linecolor)
        
        #Draw Circles
        ax.add_patch(centreCircle)
        ax.add_patch(centreSpot)
        ax.add_patch(leftPenSpot)
        ax.add_patch(rightPenSpot)
        
        #Prepare Arcs
        leftArc = Arc((11,width/2),height=20,width=20,angle=0,theta1=312,theta2=48,color=linecolor)
        rightArc = Arc((length-11,width/2),height=20,width=20,angle=0,theta1=130,theta2=230,color=linecolor)
        
        #Draw Arcs
        ax.add_patch(leftArc)
        ax.add_patch(rightArc)
                
    #Tidy Axes
    plt.axis('off')
    
    return fig,ax

def draw_lines(ax, lines, cosmetics):
    '''
    Function for drawing lines for passes between players.
    '''
    for x, y, end_x, end_y in lines:
        dx = end_x - x
        dy = end_y - y

        attributes = {
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy
        }

        ax.add_patch(patches.FancyArrow(**attributes, **cosmetics))
    
    return ax

def draw_points(ax, shots):
    '''
    Function for drawing points for each player's position.
    '''
    
    cosmetics = {
            'linewidth': 2,
            'facecolor': (0, 0, 1, 1),
            'edgecolor': (0, 0, 0, 1),
            'radius': 1.5
    }
    
    for x, y in shots:
        attributes = {
            'xy': (x, y)
        }
        ax.add_patch(patches.Circle(**attributes, **cosmetics))
    
    return ax

def show_lines(ax, lines, weights, weight_adj, fill_adj):
    '''
    Function to draw the pass lines.
    '''
    for i, e in enumerate(lines):
        cosmetics = {
            'width': weight_adj(weights[i]),
            'head_width': 0,
            'head_length': 0,
            'facecolor': (0, 0, 1, fill_adj(weights[i])),
            'edgecolor': (0, 0, 0, 0)
        }
        if weights[i] > 5:
            ax = draw_lines(ax, [e], cosmetics=cosmetics)
    
    return ax

def draw_numbers(ax, avg_location, players):
    '''
    Function for drawing number for each player's position.
    '''
    for k, v in avg_location.items():
        jersey = players[k]['jersey']
        x,y = v
        
        ax.text(x, y,
                jersey, fontsize=12,
                ha='center', va='center',
                color='white')
    
    return ax

def label_players(ax):
    '''
    Function for labeling the players.
    '''
    ## adding title
    ax.text(60, 82, 'Barcelona\'s Passinig Network || Barca vs Real Madrid (Nov 2010)', fontsize=15)
    
    ## adding labels
    ax.text(127, 80, '1 - Victor Valdes', fontsize=15)
    ax.text(127, 75, '2 - Dani Alves', fontsize=15)
    ax.text(127, 70, '3 - Gerard Pique', fontsize=15)
    ax.text(127, 65, '5 - Carles Puyol', fontsize=15)
    ax.text(127, 60, '6 - Xavi Hernandez', fontsize=15)
    ax.text(127, 55, '7 - David Villa', fontsize=15)
    ax.text(127, 50, '8 - Andres Iniesta', fontsize=15)
    ax.text(127, 45, '10 - Lionel Messi', fontsize=15)
    ax.text(127, 40, '16 - Sergio Busquets', fontsize=15)
    ax.text(127, 35, '17 - Pedro Rodriguez', fontsize=15)
    ax.text(127, 30, '22 - Eric Abidal', fontsize=15)
    
    return ax
