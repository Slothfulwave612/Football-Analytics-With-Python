"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python model for making different types of arrows.

Some parts has been taken from mplsoccer library.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Polygon

class Arrow:
    """
    a wrapper class for making arrows.
    """

    def __init__(self, arrow_type):
        """
        Function to initialize the class object.

        Args:
            arrow_type (str): type of arrow to be drawn.
        """
        self.type = arrow_type
    
    def plot_arrow(self, ax, x_start, y_start, x_end, y_end, **kwargs):
        """
        Function for plotting arrows.

        Args:
            ax (axes.Axes): axes object.
            x_start, y_start, x_end, y_end (array): starting and ending coordinates
        
        Retuns:
            axes.Axes: axes object.
        """        
        if self.type == "simple_arrows":
            return self.__plot_simple(ax, x_start, y_start, x_end, y_end, **kwargs)
        elif self.type == "cirtri":
            return self.__plot_cirtri(ax, x_start, y_start, x_end, y_end, **kwargs)
        else:
            raise TypeError("Arrow type not understood")
    
    def __plot_simple(self, ax, x_start, y_start, x_end, y_end, **kwargs):
        """
        Function to plot simple arrows using axes.Axes.quiver

        Args:
            ax (axes.Axes): axes object.
            x_start, y_start, x_end, y_end (array): starting and ending coordinates
        
        Retunrs:
            axes.Axes: axes object.
        """
        # set so plots in data units
        units = "inches"
        scale_units =  "xy"
        angles = kwargs.pop("angles", "xy")
        scale = kwargs.pop("scale", 1)
        width = kwargs.pop("width", 2)
        width = width/72    

        ## flatten arrays
        x_start = np.ravel(x_start)
        y_start = np.ravel(y_start)
        x_end = np.ravel(x_end)
        y_end = np.ravel(y_end)

        ## check for conditions
        if x_start.size != y_start.size:
            raise ValueError("x_start and y_start must be the same size")
        if x_start.size != x_end.size:
            raise ValueError("x_start and x_end must be the same size")
        if y_start.size != y_end.size:
            raise ValueError("y_start and y_end must be the same size")  
            
        ## vectors for direction
        u = x_end - x_start
        v = y_end - y_start
        
        ## add arrows
        ax.quiver(
            x_start, y_start, u, v, 
            units=units, scale_units=scale_units, angles=angles,
            scale=scale, width=width, **kwargs
        )
        
        return ax
    
    def __plot_cirtri(self, ax, x_start, y_start, x_end, y_end, **kwargs):
        """
        Function to plot simple arrows using axes.Axes.quiver

        Args:
            ax (axes.Axes): axes object.
            x_start, y_start, x_end, y_end (array): starting and ending coordinates
        
        Retunrs:
            axes.Axes: axes object.
        """        
        if kwargs.get("circle_ec") == None:
            kwargs["circle_ec"] = kwargs["circle_fc"]
        
        if kwargs.get("tri_ec") == None:
            kwargs["tri_ec"] = kwargs["tri_fc"]
        
        if kwargs.get("circle_lw") == None:
            kwargs["circle_lw"] = 1
        
        if kwargs.get("circle_alpha") == None:
            kwargs["circle_alpha"] = 1
        
        if kwargs.get("tri_alpha") == None:
            kwargs["tri_alpha"] = 1
        
        if kwargs.get("zorder") == None:
            kwargs["zorder"] = 6

        if kwargs.get("plot_first") == None:
            kwargs["plot_first"] = "circle"

        ## flatten arrays
        x_start = np.ravel(x_start)
        y_start = np.ravel(y_start)
        x_end = np.ravel(x_end)
        y_end = np.ravel(y_end)

        ## check for conditions
        if x_start.size != y_start.size:
            raise ValueError("x_start and y_start must be the same size")
        if x_start.size != x_end.size:
            raise ValueError("x_start and x_end must be the same size")
        if y_start.size != y_end.size:
            raise ValueError("y_start and y_end must be the same size")  

        for i in range(len(x_start)):
            end_x, end_y = x_end[i], y_end[i]
            start_x, start_y = x_start[i], y_start[i]

            ## traingle coordinates
            traingle_coord = self.__find_coordinates((end_x, end_y), (start_x, start_y), kwargs["radius"]) 
        
            ## add circle
            circle = Circle(
                xy = (end_x, end_y), 
                radius=kwargs["radius"], fc=kwargs["circle_fc"], ec=kwargs["circle_ec"], 
                lw=kwargs["circle_lw"], zorder=kwargs["zorder"], alpha=kwargs["circle_alpha"]
            )
            
            ## add traingle
            triangle = Polygon(
                xy=traingle_coord, fc=kwargs["tri_fc"], ec=kwargs["tri_ec"],
                zorder=kwargs["zorder"], alpha=kwargs["tri_alpha"]
            )

            if kwargs["plot_first"] == "circle":
                ax.add_patch(circle)
                ax.add_patch(triangle)
            elif kwargs["plot_first"] == "triangle":
                ax.add_patch(triangle)
                ax.add_patch(circle)

        return ax
    
    def __find_coordinates(self, head_pos, tail_pos, radius):
        """
        Function to find the coordinates for the traingle.

        Args:
            head_pos (tuple): center of the circle
            tail_pos (tuple): coordinate location of the tail.
            radius (float): radius of the circle
        
        Returns:
            tuple: the three coordinates of the triangle.(numpy array)
        """     
        ## init length of traingle
        side = 0.35

        ## init numpy arrays
        center = np.array([head_pos[0], head_pos[1]])
        point = np.array([tail_pos[0], tail_pos[1]])

        ## vector from circle's center to the point(tail_pos)
        vector = point - center

        ## first coordinates
        length = np.sqrt(vector[0]**2 + vector[1]**2)
        multiplier = radius / length
        x = center[0] + multiplier * vector[0]
        y = center[1] + multiplier * vector[1]
        temp_coord = np.array([x, y])

        ## height of the triangle
        height = side * (np.sqrt(3) / 2)

        ## rest of the coordinates
        c = (temp_coord - point) / np.linalg.norm(temp_coord - point) * height
        d = np.array([c[1], -c[0]]) / height * side / 2
        e = temp_coord + c + d
        f = temp_coord + c - d

        return (point, e, f)