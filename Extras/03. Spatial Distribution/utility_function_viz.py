# -*- coding: utf-8 -*-
"""
Created on Tue May 26 01:24:36 2020

@author: slothfulwave612

Python module for visualization.

Modules Used(1):-
1. matplotlib -- plotting library.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Arc

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