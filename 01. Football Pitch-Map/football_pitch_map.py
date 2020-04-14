'''
football_pitch_map.py
--------------------

This Python module is all about creating a football pitchmap
using the visualization module 'Matplotlib'.

Modules Used(1):
---------------
1. matplotlib -- it is a plotting library for the Python programming language

Function Defined(6):
-------------------
1. create_boundries -- for creating boundary lines of the pitch.
2. create_center_circle -- for creating center circle.
3. left_penalty_area -- for creating left penalty area.(6-yard box has separate function)
4. right_penalty_area -- for creating right penalty area.(6-yard box has separate function)
5. left_sixyard_box -- for creating six-yard box for left penalty box.
6. right_sixyard_box -- for creating six-yard box for right penalty box.
'''

## importing modules
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

## creating our figure object for our pitchmap
pitch_map = plt.figure()

## adding subplot to the figure
pitch_axis = pitch_map.add_subplot(1,1,1)

def create_boundries():
    '''
    Function will create the boundary line 
    and the middle line of the pitch with 
    the goal-post at either end of the pitch.
    '''
    ## the following lines of code will create the boundaries
    ## and the middle line of the pitchmap
    plt.plot([0,0],[0,90], color='black')
    plt.plot([0,130],[0,0], color='black')
    plt.plot([130,130],[0,90], color='black')
    plt.plot([130,0],[90,90], color='black')
    plt.plot([65,65],[0,90], color='black')

    ## the following lines of code will create 
    ## the goal-post at both side of the pitch
    plt.plot([-3,0], [40,40], color='black')
    plt.plot([-3,0], [50,50], color='black')
    plt.plot([-3,-3], [40,50], color='black')
    plt.plot([133,133], [40,50], color='black')
    plt.plot([130,133], [40,40], color='black')
    plt.plot([130,133], [50,50], color='black')

def create_center_circle():
    '''
    Function will create a circle at the 
    center of the pitchmap, with highlighting 
    the center of the circle.
    '''
    ## making a circle first by defined position
    centreCircle = plt.Circle((65,45), 9.15, color='black', fill=False)
    centreSpot = plt.Circle((65,45), 0.8, color='black')

    ## add the circle to the pitchmap
    pitch_axis.add_patch(centreCircle)
    pitch_axis.add_patch(centreSpot)

def left_penalty_area():
    '''
    Function will create the left penalty
    area of the pitchmap.
    '''
    ## left Penalty Area(without-arc)
    plt.plot([16.5,16.5],[65,25],color='black')
    plt.plot([0,16.5],[65,65],color='black')
    plt.plot([16.5,0],[25,25],color='black')

    ## making the left-arc
    left_arc = Arc((10.75,45), width=18.3, height=18.3, angle=0, theta1=310, theta2=50, color='black')

    ## adding the left arc
    pitch_axis.add_patch(left_arc)

def right_penalty_area():
    '''
    Function will create the right penalty
    area of the pitchmap.
    '''
    ## right Penalty Area(without-arc)
    plt.plot([113.5,130], [65,65], color='black')
    plt.plot([113.5,130], [25,25], color='black')
    plt.plot([113.5, 113.5], [25,65], color='black')

    ## making the right-arc
    right_arc = Arc((119.25,45), width=18.3, height=18.3, angle=180, theta1=310, theta2=50, color='black')

    ## adding the right arc
    pitch_axis.add_patch(right_arc)

def left_sixyard_box():
    '''
    Function will create the left 
    six-yard box and the spot in the penalty box.
    ''' 
    ## the six-yard box
    plt.plot([0,5.5], [54,54], color='black')
    plt.plot([0,5.5], [36,36], color='black')
    plt.plot([5.5,5.5], [54,36], color='black')

    ## creating the penalty-box spot
    penalty_spot = plt.Circle((11,45), radius=0.8, color='black')

    ## adding the spot to the penalty box
    pitch_axis.add_patch(penalty_spot)
    
def right_sixyard_box():
    '''
    Function will create the right 
    six-yard box and the spot in the penalty box.
    ''' 
    ## the six-yard box
    plt.plot([130,124.5], [54,54], color='black')
    plt.plot([130,124.5], [36,36], color='black')
    plt.plot([124.5,124.5], [54,36], color='black')

    ## creating the penalty-box spot
    penalty_spot = plt.Circle((119,45), radius=0.8, color='black')

    ## adding the spot to the penalty box
    pitch_axis.add_patch(penalty_spot)


## calling all the functions to create the pitch map.

create_boundries()         
## to create the boundary lines

create_center_circle()      
## to create the center circle

left_penalty_area()
## to create the left-penalty box

right_penalty_area()
## to create the right-penalty box

left_sixyard_box()
## to create the left-penalty six-yard box

right_sixyard_box()
## to create the right-penalty six-yard box

plt.show()
## to display the plot on the screen

## Slothfulwave612...
