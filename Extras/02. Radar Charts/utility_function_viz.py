# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:27:24 2020

@author: slothfulwave612

Python module for visualization.

Got this code from stackexchange.
@kyler_brown

Modules Used(1):-
1. numpy -- numerical computing library.
2. matplotlib -- plotting library.
"""
import numpy as np
import matplotlib.pyplot as plt

class RadarChart():
    '''
    a class for making radar charts.
    '''
    
    def __init__(self, fig, params, ranges):
        '''
        Function for initializing class objects.
        
        Arguments:
        fig -- figure object.
        params -- list of parameters(or player attributes).
        ranges -- list containing tuple of ranges to be shown in the plot.
        '''
        fig = plt.figure(figsize=(6,6))
        
        angles = np.arange(0, 360, 360 / len(params))
        
        axes = [ fig.add_axes([0.1, 0.1, 0.9, 0.9], polar=True,
                label = "axes{}".format(i)) 
                for i in range(len(params)) ]
        
        l, text = axes[0].set_thetagrids(angles, 
                                      labels=params)
        
        n_ordinate_levels = [txt.set_rotation(angle-90) for txt, angle 
                                      in zip(text, angles)]
        
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid(False)
            ax.xaxis.set_visible(False)
        
        
        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i], 
                               num=n_ordinate_levels)
            
            gridlabel = ["{}".format(round(x,2)) 
                         for x in grid]
            
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1] # hack to invert grid
                          # gridlabels aren't reversed
                          
            gridlabel[0] = "" # clean up origin
            
            ax.set_rgrids(grid, labels=gridlabel,
                         angle=angles[i])
            
            #ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
            
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        