"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module for creating heatmaps.

Some parts taken from mplsoccer.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.stats import binned_statistic_2d
from scipy.stats import circmean

from . import Pitch, my_utils, Arrows

class Heatmap:
    """
    a wrapper class for making heatmaps.
    """

    def __init__(
        self, pass_flow=False, line_color="#121212", pitch_color="#F5F5F5", orientation="horizontal", 
        cmap="Blues", show=True, arrow_length=4, color="#121212", arrow_type="same", arrow_order=4, normalize=False,
        arrow_color="#121212", alpha=1, plot=None, interpolation=None
    ):
        """
        Function to initialize the object of the class.

        Args:
            pass_flow (bool, optional): to make pass flow charts. Defaults to False.
            line_color (str, optional): line color for the pitch. Default to "#121212".
            pitch_color (str, optional): color of the pitch. Defaults to "#F5F5F5".
            orientation (str, optional): orientation of the pitch. Defaults to "horizontal".
            cmap (str/list, optinal): color palette for the heatmap. Defaults to "Blues".
                                      list for user defined color map.
            show (bool, optional): to show the plot on screen. Defaults to True.
            arrow_length (float, optional): arrow length for the pass flow. Defaults to 4.
            color (str, optional): color for the arrows. Defaults to "#121212".
            arrow_type (str, optional): type of arrow to be plotted. Defaults to "same.
            arrow_order (int, optional): zorder for arrows. Default to 4.
            normalize (bool, optional): to normalize heatmap or not. Defaults to False.
            arrow_color (str, optional): the color of the arrows. Defaults to "#121212".
            alpha (float, optional): alpha value for our heatmap. Defaults to 1.
            plot (str, optional): to plot the points. Defauts to None.
            interpolation (str, optional): interpolation. Default to "none".
        """        
        self.pass_flow = pass_flow
        self.line_color = line_color
        self.pitch_color = pitch_color
        self.orientation = orientation
        self.cmap=cmap
        self.show = show
        self.arrow_length = arrow_length
        self.color = color
        self.arrow_type = arrow_type
        self.arrow_order=4
        self.normalize = normalize
        self.arrow_color = arrow_color
        self.alpha = alpha
        self.plot = plot
        self.interpolation = interpolation

        if type(self.cmap) == list:
            self.cmap = colors.ListedColormap(self.cmap)

    def make_heatmap(self, df, heat_type, bins=(6,4), filename=None, zorder=2, **kwargs):
        """
        Function for making heatmap.

        Args:
            df (pandas.DataFrame): event dataframe.
            heat_type (str): type of heatmap to be plotted.
            bins (tuple, optional): containing partitions of the pitch in x and y axis respectively. Defaults to (6,4).
            filename (str, optional): path where plot will be saved. Defaults to None.
            zorder (int, optional): zorder for our heatmap. Defaults to 2.
            **kwargs (dict, optional): dict will contain following parameters.
                image_path (str, optional): path of the image.
                orientation_array (list, optional): array defining where the image will be plotted. e.g. to [0.14, 0.629, 0.1, 0.03].
                main_title (str, optional): title of the plot.
                sub_title (str, optional): sub-title of the plot.
                credit (str): credit at the end. Defaults to None.
                main_coord (tuple, optional): coordinates for main title. Defaults to e.g. (9, 109.5).
                sub_coord (tuple, optional): coordinates for sub title. Defaults to e.g. (9, 107).
                credit_coord (tuple, optional): coordinates for credits. Defaults to e.g. (68, 50.5).
                font (str, optional): fontfamliy to be used. e.g. "Liberation Serif"
                figax (tuple, optional): contains fig and axes object. 

        Returns:
            axes.Axes: axes object.
        """        
        ## init object of Pitch class
        pitch = Pitch.Pitch(
            line_color=self.line_color, pitch_color=self.pitch_color, orientation=self.orientation,
            plot_arrow=True
        )

        ## create pitch map
        if kwargs.get("figax"):
            fig, ax = pitch.create_pitch(figax=kwargs["figax"])
        else:
            fig, ax = pitch.create_pitch()

        ## plot heatmap
        if heat_type == "simple_heatmap":
            ax = self.create_heatmap(df, ax, bins, filename, zorder)

        ## add image to the figure
        if kwargs.get("image_path"):
            fig = my_utils.add_image(
                kwargs["image_path"], fig, kwargs["orientation_array"][0],
                kwargs["orientation_array"][1], kwargs["orientation_array"][2],
                kwargs["orientation_array"][3]
            )

        ## plot title
        if kwargs.get("main_coord") and kwargs.get("main_title"):
            ax.text(
                kwargs["main_coord"][0], kwargs["main_coord"][1], kwargs["main_title"],
                fontsize=kwargs["main_size"], fontweight="bold", color="#ececec", fontfamily=kwargs["font"]
            )

        ## plot sub-title
        if kwargs.get("sub_coord") and kwargs.get("sub_title"):
            ax.text(
                kwargs["sub_coord"][0], kwargs["sub_coord"][1], kwargs["sub_title"],
                fontsize=kwargs["sub_size"], fontweight="bold", color="#ececec", fontfamily=kwargs["font"]
            )

        ## add credits
        if kwargs.get("credit_coord") and kwargs.get("credit"):
            ax.text(
                kwargs["credit_coord"][0], kwargs["credit_coord"][1], kwargs["credit"],  
                fontsize=kwargs["credit_size"], color="#ececec", fontstyle="italic", fontfamily="Liberation Serif", ha="right", va="center"
            )

        if filename:
            fig.savefig(
                filename, dpi=500, bbox_inches="tight",
                facecolor=fig.get_facecolor()
            )

        if self.show == False:
            plt.close("all")
        elif self.show == True:
            plt.show()

        return fig, ax
    
    def create_heatmap(self, df, ax, bins=(6,4), filename=None, zorder=2):
        """
        Helper function to create heatmap.

        Args:
            df (pandas.DataFrame): event dataframe.
            bins (tuple, optional): containing partitions of the pitch in x and y axis respectively. Defaults to (6,4).
            filename (str, optional): path where plot will be saved. Defaults to None.
            zorder (int, optional): zorder for our heatmap. Defaults to 2.

        Returns:
            axes.Axes: axes object.
        """        
        ## get required matrix
        matrix = self.make_matrix(df, bins, ax)
        
        ## plotting heatmap on the pitch
        ax.imshow(
            matrix, zorder=zorder, aspect="auto", vmin=0, vmax=matrix.max(), 
            extent=(0, 104, 0, 68), cmap=self.cmap, alpha=self.alpha, interpolation=self.interpolation
        )
        
        ## edit xticks
        ax.set_xticks([-3, 106])
        ax.set_yticks([-3, 74])

        if self.pass_flow == True:
            self.make_plot_flow(df, bins, ax)
        
        return ax

    def create_aligned_heatmap(self, df, bins=(4,4), filename=None, zorder=2):
        """
        Function for making aligned heatmap.

        Args:
            df (pandas.DataFrame): event dataframe.
            bins (tuple, optional): containing partitions of the pitch in x and y axis respectively. Defaults to (4,4).
            filename (str, optional): path where plot will be saved. Defaults to None.
            dpi (int, optional): dots per inch value. Defaults to 500.
            bbox_inches (str, optional): bounding box in inches. Defaults to "tight".
            zorder (int, optional): zorder for our heatmap. Defaults to 2.

        Returns:
            pyplot.Figure: figure object.
            axes.Axes: axes object.
        """
        ## create pitch map
        pitch = Pitch.Pitch(
            line_color=self.line_color, pitch_color=self.pitch_color, orientation=self.orientation,
            plot_arrow=True, arrow_color=self.arrow_color
        )
        fig, ax = pitch.create_pitch()

        ## get required matrix
        array_left, matrix, array_right = self.make_aligned_matrix(df, bins)

        ## calculate max value
        max_val = max(
            array_left.max(), matrix.max(), array_right.max()
        )
        
        ## plotting heatmap on the pitch -- for left array
        ax.imshow(np.zeros((3,1)) + array_left[0], zorder=zorder, aspect="auto", vmin=0, vmax=max_val, 
        extent=(0, 16.5, 54.16, 68), cmap=self.cmap, alpha=self.alpha)
        ax.imshow(np.zeros((3,1)) + array_left[1], zorder=zorder, aspect="auto", vmin=0, vmax=max_val, 
        extent=(0, 16.5, 13.84, 54.15), cmap=self.cmap, alpha=self.alpha)
        ax.imshow(np.zeros((3,1)) + array_left[2], zorder=zorder, aspect="auto", vmin=0, vmax=max_val, 
        extent=(0, 16.5, 0, 13.83), cmap=self.cmap, alpha=self.alpha)

        ## plotting heatmap on the pitch -- for matrix
        ax.imshow(matrix, zorder=zorder, aspect="auto", vmin=0, vmax=max_val, extent=(16.5, 87.5, 0, 68), cmap=self.cmap, alpha=self.alpha)

        ## plotting heatmap on the pitch -- for left array
        ax.imshow(np.zeros((3,1)) + array_right[0], zorder=zorder, aspect="auto", vmin=0, vmax=max_val, 
        extent=(87.51, 104, 54.16, 68), cmap=self.cmap, alpha=self.alpha)
        ax.imshow(np.zeros((3,1)) + array_right[1], zorder=zorder, aspect="auto", vmin=0, vmax=max_val, 
        extent=(87.5, 104, 13.84, 54.15), cmap=self.cmap, alpha=self.alpha)
        ax.imshow(np.zeros((3,1)) + array_right[2], zorder=zorder, aspect="auto", vmin=0, vmax=max_val, 
        extent=(87.5, 104, 0, 13.83), cmap=self.cmap, alpha=self.alpha)

        ## edit xticks
        ax.set_xticks([-2, 106])
        ax.set_yticks([-2, 70])

        # if self.pass_flow == True:
        #     self.make_plot_flow(df, bins, ax)

        if filename:
            fig.savefig(filename, dpi=500, bbox_inches="tight")
        
        if self.show == False:
            plt.close("all")
        elif self.show == True:
            plt.show()
        
        return fig, ax

    def make_aligned_matrix(self, df, bins=(4,4), ax=None, zorder=4):
        """
        Function for making the required matrix for plotting aligned-heatmap.

        Args:
            df (pandas.DataFrame): event dataframe.
            bins (tuple, optional): containing partitions of the pitch in x and y axis respectively. Defaults to (4,4).
            ax (axes.Axes, optional): axes object. Deafults to None.
            zorder (int, optional): zorder for scatter points. Defaults to None.

        Returns:
            numpy.ndarray: required matrix.
        """        
        ## init two arrays and one matrix
        array_left = np.zeros(shape=(3,))
        matrix = np.zeros(shape=(4,4))
        array_right = np.zeros(shape=(3,))

        for _, data in df.iterrows():
            ## fetch start location
            x_start, y_start = data['x'], data['y']

            ## for array_left
            if 0 <= x_start < 16.5:
                if 0 <= y_start < 13.84:
                    array_left[2] += 1
                elif 13.84 <= y_start < 54.16:
                    array_left[1] += 1
                elif 54.16 <= y_start <= 68:
                    array_left[0] += 1
                
            ## for matrix
            elif 16.5 <= x_start <= 87.5:
                ## convert dims
                x = my_utils.change_dims(x_start, 16.5, 87.5, 0, 71)

                ## get indices
                x_idx, y_idx = my_utils.get_indices(71, 68, 4, 4, x, y_start)

                ## increment matrix
                matrix[x_idx, y_idx] += 1
            
            ## for right array
            elif 87.51 <= x_start <= 104:
                if 0 <= y_start < 13.84:
                    array_right[2] += 1
                elif 13.84 <= y_start < 54.16:
                    array_right[1] += 1
                elif 54.16 <= y_start <= 68:
                    array_right[0] += 1

        return array_left, matrix, array_right


    def make_matrix(self, df, bins, ax=None, zorder=4):
        """
        Function for making the required matrix for plotting heatmap.

        Args:
            df (pandas.DataFrame): event dataframe.
            bins (tuple): containing partitions of the pitch in x and y axis respectively.
            ax (axes.Axes): axes object. Deafults to None.
            zorder (int): zorder for scatter points. Defaults to None.

        Returns:
            numpy.ndarray: required matrix.
        """        
        ## init a zero matrix
        matrix = np.zeros(shape=(bins[1], bins[0]))

        ## traverse the dataframe
        for _, data in df.iterrows():
            ## get indices for the matrix
            x, y = my_utils.get_indices(
                width=104, height=68, x_partition=bins[0], y_partition=bins[1], 
                xinput=data['x'], yinput=data['y']
            )

            if self.plot:
                ax.scatter(data['x'], data['y'], color=self.plot, zorder=zorder, marker='.', s=8)

            ## increment by one
            matrix[x, y] += 1
        
        return matrix

    def make_plot_flow(self, df, bins, ax):
        """
        Function to plot the arrows for each bin.

        Args:
            df (pandas.DataFrame): event dataframe
            bins (tuple): containing partitions of the pitch in x and y axis respectively.
            ax (axes.Axes): axes object.
        
        Returns:
            axes.Axes: axes object
        """        
        ## valid arrow type available
        valid_arrows = ["same", "average"]

        if self.arrow_type not in valid_arrows:
            raise TypeError(f"Invalid argument: arrow_type should be in {valid_arrows}")
        
        ## start and end location
        x_start = df["x"]
        y_start = df["y"]
        x_end = df["endX"]
        y_end = df["endY"]

        ## calculate angle and distance
        angle, distance = self.calculate_angle_and_distance(x_start, y_start, x_end, y_end)
        bin_distance = self.bin_statistics(x_start, y_start, bins, values=distance, statistic="mean")
        bin_angle = self.bin_statistics(x_start, y_start, bins, values=angle, statistic=circmean)

        if self.arrow_type == 'same':
            new_d = self.arrow_length
        elif self.arrow_type == 'average':
            new_d = bin_distance['statistic']
        
        ## calculate end_x and end_y respectively
        end_x = bin_angle['cx'] + (np.cos(bin_angle['statistic']) * new_d)  
        end_y = bin_angle['cy'] + (np.sin(bin_angle['statistic']) * new_d)

        ## plot arrows
        arrow = Arrows.Arrow(arrow_type="simple_arrows")
        ax = arrow.plot_arrow(ax, bin_angle["cx"], bin_angle["cy"], end_x, end_y, headlength=10, headwidth=10, zorder=self.arrow_order, color=self.arrow_color)

        return ax
    
    def calculate_angle_and_distance(self, x_start, y_start, x_end, y_end):
        """
        Function to calculate angle and distance.

        Args:
            x_start, y_start, x_end, y_end (array): starting and ending coordinates

        Returns:
            angle, distance
        """        
        ## flatten the array
        x_start = np.ravel(x_start)
        y_start = np.ravel(y_start)
        x_end = np.ravel(x_end)
        y_end = np.ravel(y_end)

        ## check some conditions
        if x_start.size != y_start.size:
            raise ValueError("x_start and y_start must be the same size")
        if x_start.size != x_end.size:
            raise ValueError("x_start and x_end must be the same size")
        if y_start.size != y_end.size:
            raise ValueError("y_start and y_end must be the same size")  
        
        ## distance in x and y direction respectively
        x_dist = x_end - x_start
        y_dist = y_end - y_start

        ## calculate angle
        angle = np.arctan2(y_dist, x_dist)
        
        # if negative angle make positive angle, so goes from 0 to 2 * pi
        angle[angle < 0] = 2 * np.pi + angle[angle < 0]

        ## calculate distance
        distance = (x_dist**2 + y_dist**2) ** 0.5

        return angle, distance

    def bin_statistics(self, x, y, bins, values=None, statistic="count"):
        """
        Function to find bin statistics.

        Args:
            x, y (array-like, scalar)
            bins (tuple): containing partitions of the pitch in x and y axis respectively.
            statistic (str, optional): the statistics to count. Defaults to "count".

        Returns:
            bin_statistic (dict): the keys are "statistics"(the calculated statistics).
                                   "x_grid" and "y_grid" (the bin's edges), and cx and cy (the bin centers).
        """                        
        ## flatten the array
        x = np.ravel(x)
        y = np.ravel(y)

        if x.size != y.size:
            raise ValueError("x and y must be the same size")

        if values is not None:
            values = np.ravel(values)
            
        if (values is None) & (statistic == 'count'):
            values = x
            
        if (values is None) & (statistic != 'count'):
            raise ValueError("values on which to calculate the statistic are missing")
        
        if values.size != x.size:
            raise ValueError("x and values must be the same size")
            
        ## pitch range
        if self.orientation == "horizontal":
            pitch_range = [[0, 104], [0, 68]]
        elif self.orientation == "vertical":
            pitch_range = [[0, 68], [0, 104]]
        else:
            raise ValueError("Orientation type not understood")

        ## calculate binned statistics using scipy
        result = binned_statistic_2d(x, y, values, statistic=statistic, bins=bins, range=pitch_range)

        statistic = result.statistic.T
        x_grid, y_grid = np.meshgrid(result.x_edge, result.y_edge)
        cx, cy = np.meshgrid(result.x_edge[:-1] + 0.5 * np.diff(result.x_edge),
                             result.y_edge[:-1] + 0.5 * np.diff(result.y_edge))
        
        ## make dict
        bin_statistic = dict(
            statistic=statistic, x_grid=x_grid, y_grid=y_grid, cx=cx, cy=cy
        )

        return bin_statistic

        