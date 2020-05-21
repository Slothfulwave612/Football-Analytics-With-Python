# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:27:24 2020

@author: slothfulwave612

Python module for visualization.

Got this code from stackexchange.
@kyler_brown

Modules Used(1):-
1. numpy -- numerical computing library.
2. matplotlib -- plotting library in python.
"""
import numpy as np
import matplotlib.pyplot as plt

def _invert(x, limits):
    '''
    inverts a value x on a scale from
    limits[0] to limits[1]
    '''
    return limits[1] - (x - limits[0])

class ComplexRadar():
    '''
    A class to plot a complex radar chart.
    '''
    
    def __init__(self, fig, variables, ranges, n_ordinate_levels=6):
        '''
        Function to initialize the class object.
        
        Arguments:
        fig -- figure object.
        variables -- list, the labels.
        ranges -- list, of ranges of each labels.
        '''
        angles = np.arange(0, 360, 360./len(variables))

        axes = [fig.add_axes([0.1,0.1,0.9,0.9], polar=True,
            label = "axes{}".format(i)) 
            for i in range(len(variables))]

        l, text = axes[0].set_thetagrids(angles, labels=variables)

        [[txt.set_fontweight('bold'),
              txt.set_fontsize(12),
              txt.set_position((0,-0.2))] for txt in text]

        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid(False)
            ax.xaxis.set_visible(False)

        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i], num=n_ordinate_levels)
            gridlabel = ["{}".format(round(x,2)) for x in grid]

            gridlabel[0] = "" # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,angle=angles[i])

            ax.set_ylim(*ranges[i])
        
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]

    def plot(self, data, *args, **kw):
        '''
        Function to plot the data.
        
        Argument:
        data -- list, data to be plotted.
        '''
        sdata = self.scale_data(data, self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

    def fill(self, data, *args, **kw):
        '''
        Function to fill the plot.
        
        Argument:
        data -- list, data to be plotted.
        '''
        sdata = self.scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

    def scale_data(self, data, ranges):
        '''
        Function to scales data[1:] to ranges[0].
        
        Arguments:
        data -- list, data to be plotted.
        ranges -- list, range for each label.
        '''
        for d, (y1, y2) in zip(data[1:], ranges[1:]):
            assert (y1 <= d <= y2) or (y2 <= d <= y1)
            
        x1, x2 = ranges[0]
        d = data[0]
        sdata = [d]
        
        for d, (y1, y2) in zip(data[1:], ranges[1:]):
            
            if y1 > y2:
                d = _invert(d, (y1, y2))
                y1, y2 = y2, y1
            sdata.append((d-y1) / (y2-y1) * (x2 - x1) + x1)
            
        return sdata
    
def plot_player_data(labels, ranges, stats, title='radar_chart', save_title='radar_save'):
    '''
    Function to plot player's data.
    
    Arguments:
    labels -- list, of parameters.
    ranges -- list, of ranges for each parameter/label.
    stats -- list, of statistics for each player.
    title -- str, title of the radar plot.
    save_title -- str, name while saving the radar plot.
    '''
    plt.style.use('ggplot')
    
    fig = plt.figure(figsize=(8, 8))
    radar = ComplexRadar(fig, labels, ranges)
    radar.plot(stats)
    radar.fill(stats, alpha=0.2)
    
    fig.suptitle(title, x=0.1, y=1.16, fontsize=20, color='#444444')
    fig.savefig(save_title, bbox_inches='tight')
