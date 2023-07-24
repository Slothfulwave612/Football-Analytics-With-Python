"""
__author__: Anmol_Durgapal(@slothfulwave612)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle, Arc

import Arrows

class Pitch:
    '''
    class to create a pitch-map.
    
    Pitch Dimensions: 104x64 (in meters)
    '''
    
    def __init__(
        self, line_color="#000000", pitch_color="#FFFFFF", orientation="horizontal", 
        half=False, plot_arrow=True, arrow_color="#9C9C9C", sxy=(20, 16)
        ):
        """
        Function to initialize the object of the class.

        Args:
            line_color (str, optional): line color of pitch-map. Defaults to "#000000".
            pitch_color (str, optional): pitch color of pitch-map. Defaults to "#FFFFFF".
            orientation (str, optional): orientation of the pitch-map. Defaults to "horizontal".
            half (bool, optional): to plot half-pitch. Defaults to False.
            plot_arrow (bool, optional): to plot arrow. Defaults to True.
            arrow_color (str, optional): color of the arrow to be plotted. Defaults to "#9C9C9C".
            sxy (tuple, optional): size of the pitch. Defaults to (20, 16).
        """        
        
        self.line_color = line_color
        self.pitch_color = pitch_color
        self.orientation = orientation
        self.half = half
        self.plot_arrow = plot_arrow
        self.arrow_color = arrow_color
        self.sxy = sxy
        
        ## pitch outfield lines
        self.pitch_dims = [
            [0, 104, 104, 0, 0],           ## x-axis
            [0, 0, 68, 68, 0]              ## y-axis
        ]
        
        self.dims_x = [
            [104, 87.5, 87.5, 104],        ## right-side penalty box(x-axis)
            [0, 16.5, 16.5, 0],            ## left-side penalty box(x-axis)
            [104, 105.5, 105.5, 104],      ## right-side goal post(x-axis)
            [0, -1.5, -1.5, 0],            ## left-side goal post(x-axis)
            [104, 99.5, 99.5, 104],        ## right-side 6-yard-box(x-axis)
            [0, 4.5, 4.5, 0]               ## left-side 6-yard-box(x-axis)
        ]
        
        self.dims_y = [
            [13.84, 13.84, 54.16, 54.16],  ## right-side penalty box(y-axis)
            [13.84, 13.84, 54.16, 54.16],  ## left-side penalty box(y-axis)
            [30.34, 30.34, 37.66, 37.66],  ## right-side goal post(y-axis)
            [30.34, 30.34, 37.66, 37.66],  ## left-side goal post(y-axis)
            [24.84, 24.84, 43.16, 43.16],  ## right-side 6-yard-box(y-axis)
            [24.84, 24.84, 43.16, 43.16]   ## left-side 6-yard-box(y-axis)
        ]
        
        self.half_x = [52, 52]             ## halfway line x-axis
        self.half_y = [0, 68]              ## halfway line y-axis
        
        self.scatter_x = [93, 10.5, 52]    ## penalty and kick off spot(x-axis)
        self.scatter_y = [34, 34, 34]      ## penalty and kick off spot(y-axis)
        
    def create_pitch(self, zorder_line=3, figax=None):
        '''
        Function to create pitch-map.
        
        Arguments:
            self -- represents the object of the class.
            zorder_line -- int, zorder value for pitch-lines.
            fill_rect -- list of x and y coordinates for the rectangle.
            length -- float, length of the rectangle.
            bredth -- float, bredth of the rectangle.
        
        Returns:
            fig, ax -- figure and axis object.
        '''
        
        if self.orientation == 'horizontal':
            ## figsize
            sx, sy = self.sxy[0], self.sxy[1]
            
            ## x and y coordinates for pitch outline
            pitch_dims_x = self.pitch_dims[0]
            pitch_dims_y = self.pitch_dims[1]
            
            ## x and y coordinates for halfway line
            half_x = self.half_x
            half_y = self.half_y
            
            ## x and y coordinate list
            x_coord = self.dims_x
            y_coord = self.dims_y
            
            ## x and y coordinate for spots
            spot_x = self.scatter_x
            spot_y = self.scatter_y
            
            
        elif self.orientation == 'vertical':
            ## figsize
            sx, sy = self.sxy[1], self.sxy[0]
            
            ## x and y coordinates for pitch outline
            if self.half == False:
                pitch_dims_x = self.pitch_dims[1]
                pitch_dims_y = self.pitch_dims[0]
            else:
                pitch_dims_x = [0, 0, 68, 68]
                pitch_dims_y = [52, 104, 104, 52]
            
            ## x and y coordinates for halfway line
            half_x = self.half_y
            half_y = self.half_x
            
            ## x and y coordinate list
            x_coord = self.dims_y
            y_coord = self.dims_x
        
            ## x and y coordinate for spots
            spot_x = self.scatter_y
            spot_y = self.scatter_x 
        
        else:
            raise Exception('Orientation not understood!!!')
        
        if figax == None:
            ## create subplot
            fig, ax = plt.subplots(figsize=(sx, sy), facecolor=self.pitch_color)
            ax.set_facecolor(self.pitch_color)
            ax.set_aspect("equal")
        else:
            fig, ax = figax[0], figax[1]

        if self.plot_arrow == True and self.orientation == "horizontal":
            arrow = Arrows.Arrow(arrow_type="simple_arrows")
            ax = arrow.plot_arrow(
                ax, 40, -1.5, 64, -1.5, color=self.arrow_color,
                width=2, headlength=5, headwidth=5, zorder=4
            )
        
        elif self.plot_arrow == True and self.orientation == "vertical":
            arrow = Arrows.Arrow(arrow_type="simple_arrows")
            ax = arrow.plot_arrow(
                ax, -2, 40, -2, 64, color=self.arrow_color,
                width=2, headlength=5, headwidth=5, zorder=4
            )

        ## plot outfield lines
        ax.plot(pitch_dims_x, pitch_dims_y, color=self.line_color, zorder=zorder_line, lw=2)
        
        ## plot right side penalty box
        ax.plot(x_coord[0], y_coord[0], color=self.line_color, zorder=zorder_line, lw=2)            
        
        ## plot right side goal post
        ax.plot(x_coord[2], y_coord[2], color=self.line_color, zorder=zorder_line, lw=2)                
        
        ## right hand 6 yard box
        ax.plot(x_coord[4], y_coord[4], color=self.line_color, zorder=zorder_line, lw=2)                
        
        ## plot halfway line
        ax.plot(half_x, half_y, color=self.line_color, zorder=zorder_line, lw=2)

        if self.half == False:
            ## plot left side penalty box
            ax.plot(x_coord[1], y_coord[1], color=self.line_color, zorder=zorder_line, lw=2)

            ## plot left side goal post
            ax.plot(x_coord[3], y_coord[3], color=self.line_color, zorder=zorder_line, lw=2)

            ## left side 6 yard box
            ax.plot(x_coord[5], y_coord[5], color=self.line_color, zorder=zorder_line, lw=2)

            ## kick-off spot
            ax.scatter(spot_x[1], spot_y[1], color=self.line_color, s=10, zorder=zorder_line, lw=2)
        
        ## plot penalty 
        ax.scatter(spot_x[0], spot_y[0], color=self.line_color, s=10, zorder=zorder_line, lw=2)
        # ax.scatter(spot_x[2], spot_y[2], color=self.line_color, s=10, zorder=zorder_line, lw=2)
        
        if self.half == False:
            ## plot center circle
            circle = plt.Circle((spot_x[2], spot_y[2]), 9.15, lw=2, color=self.line_color, 
                                fill=False, zorder=zorder_line)
            ax.add_patch(circle)
        else:
            ## draw center arc
            arc = Arc(xy=(34, 52), height=18.5, width=18.5, angle=90, theta1=270, theta2=90, color=self.line_color, zorder=zorder_line, lw=2)
            ax.add_patch(arc)

        ## adding arcs
        if self.orientation == "horizontal":
            arc_left = Arc(xy=(10.5, 34), height=18.5, width=18.5, angle=0, theta1=310, theta2=50, color=self.line_color, zorder=zorder_line, lw=2)
            arc_right = Arc(xy=(93.5, 34), height=18.5, width=18.5, angle=0, theta1=130, theta2=230, color=self.line_color, zorder=zorder_line, lw=2)

            ax.add_patch(arc_left)
            ax.add_patch(arc_right)
        
        elif self.orientation == "vertical":
            if self.half == False:
                arc_bottom = Arc(xy=(34, 10.5), height=18.5, width=18.5, angle=90, theta1=310, theta2=50, color=self.line_color, zorder=zorder_line, lw=2)
                ax.add_patch(arc_bottom)

            arc_top = Arc(xy=(34, 93.5), height=18.5, width=18.5, angle=90, theta1=130, theta2=230, color=self.line_color, zorder=zorder_line, lw=2)
            ax.add_patch(arc_top)

        if self.orientation == "vertical" and self.half == True and self.plot_arrow == False:
            ax.set(ylim=(50, 106))

        ## tidy axis
        ax.axis('off')
        
        return fig, ax


