"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module for creating heatmaps.

Some parts taken from mplsoccer.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

import Pitch, my_utils, Arrows

def element(x):
    return x[0], x[1]

class Heatmap:
    """
    a wrapper class for making heatmaps.
    """

    def __init__(self, total_touches):
        """
        <--- constructor --->

        Args:
            total_touches (int): total number of touches.
        """
        self.total_touches = total_touches

    def make_matrix(
        self, df, bins, width, height, columns=['x', 'y']
    ):
        """
        Function for making the required matrix for plotting heatmap.

        Args:
            df (pandas.DataFrame): event dataframe.
            bins (tuple): containing partitions of the pitch in x and y axis respectively.
            width (float): width of the pitch.
            height (float): height of the pitch.

        Returns:
            numpy.ndarray: required matrix.
        """

        def matrix_inc(x):
            matrix[x[0], x[1]] += 1

        # init a zero matrix
        matrix = np.zeros(
            shape=[bins[1], bins[0]]
        )

        # compute 
        df[[columns[0], columns[1]]].apply(
            lambda x: my_utils.get_indices(
                width, height, bins[0], bins[1], element(x)[0], element(x)[1]
            ), axis=1
        ).apply(
            lambda x: matrix_inc(x)
        )

        return matrix

    def make_matrix_pen(self, df, def_area=False):
        """
        Function for making the required matrix 
        for attacking penalty area.

        Args:
            df (pandas.DataFrame): event dataframe.
            def_area (bool, optional): plot on defensive area. Defaults to False.

        Returns:
            numpy.ndarray: required matrix.
        """
        
        def matrix_inc(x):
            x, y = x[0], x[1]

            if def_area:
                cond = y <= 16.5
            else:
                cond = y >= 87.5

            if cond:
                if x <= 13.84:
                    matrix[0, 0] += 1
                elif 13.84 < x <= 54.16:
                    matrix[0, 1] += 1
                elif 54.16 < x <= 68:
                    matrix[0, 2] += 1
        
        # init a zero matrix
        matrix = np.zeros(
            shape=[1, 3]
        )

        df[['x', 'y']].apply(
            lambda x: matrix_inc(x), axis=1
        )

        return matrix

    def make_matrix_opp(self, df, def_area=False):
        """
        Function for making the required matrix
        for opponent area. (excluding penalty area)

        Args:
            df (pandas.DataFrame): event dataframe.
            def_area (bool, optional): plot on defensive area. Defaults to False.
        
        Returns:
            numpy.ndarray: required matrix
        """

        def matrix_inc(x):
            x, y = x[0], x[1]

            if def_area:
                if 34.25 <= y < 52:
                    index = 0
                elif 16.5 < y < 34.25:
                    index = 1
                else:
                    return
            else:
                if 69.75 <= y < 87.5:
                    index = 0
                elif 52 <= y < 69.75:
                    index = 1
                else:
                    return

            if 0 <= x <= 13.84:
                matrix[index, 0] += 1
            elif 13.84 < x <= 54.16:
                matrix[index, 1] += 1
            elif 54.16 < x <= 68:
                matrix[index, 2] += 1

        # init a zero matrix
        matrix = np.zeros(
            shape=[2, 3]
        )

        df[['x', 'y']].apply(
            lambda x: matrix_inc(x), axis=1
        )

        return matrix
    
    def make_matrix_halfspace(self, df):
        """
        Function for making the required matrix
        for opponent area. (excluding penalty area)
        Incorporating halfspaces.

        Args:
            df (pandas.DataFrame): event dataframe.
            def_area (bool, optional): plot on defensive area. Defaults to False.
        
        Returns:
            numpy.ndarray: required matrix
        """

        def matrix_inc(x):
            x, y = x[0], x[1]

            if 69.75 <= y < 87.5:
                index = 0
            elif 52 <= y < 69.75:
                index = 1
            else:
                return

            if 0 <= x <= 13.84:
                matrix[index, 0] += 1
            elif 13.84 < x <= 24.84:
                matrix[index, 1] += 1
            elif 24.84 < x <= 43.16:
                matrix[index, 2] += 1
            elif 43.16 < x <= 54.16:
                matrix[index, 3] += 1
            elif 54.16 < x <= 68:
                matrix[index, 4] += 1

        # init a zero matrix
        matrix = np.zeros(
            shape=[2, 5]
        )

        df[['x', 'y']].apply(
            lambda x: matrix_inc(x), axis=1
        )

        return matrix

    def show_pen(
        self, matrix, ax, kwargs_show, kwargs_text, 
        def_area=False, annotate=False, show_zero=True
    ):
        """
        Function to superimpose a matrix on pitch
        in the penalty area.

        Args:
            matrix (numpy.ndarray): required matrix
            ax (axes.Axes): axes object.
            kwargs_show: all value to axes.Axes.imshow().
            kwargs_text: all value to axes.Axes.text().
            def_area (bool, optional): plot on defensive area. Defaults to False.
            annotate (bool, optional): to annotate the heatmap.

        Returns:
            axes.Axes: axes object
        """
        x_coord = [0, 13.84, 54.16, 68]

        if def_area:
            start_y, end_y = 0, 16.5
        else:
            start_y, end_y = 87.5, 104
            
        # get required x coordinates
        x = [(x, y) for x, y in zip(x_coord[:-1], x_coord[1:])]

        if annotate:
            matrix_per = np.round(matrix / self.total_touches * 100, 1)

        for index, val in enumerate(x):
            if not show_zero and matrix_per[0, index] == 0:
                continue

            ax.imshow(
                [[matrix[0,index]]], extent=[val[0], val[1], start_y, end_y], **kwargs_show
            )

            if annotate:
                ax.text(
                    (val[0] + val[1]) / 2, (start_y + end_y) / 2,
                    str(matrix_per[0, index]) + '%', **kwargs_text
                )

        return ax
    
    def show_opp(
        self, matrix, ax, kwargs_show, kwargs_text,
        def_area=False, annotate=False
    ):
        """
        Function to superimpose a matrix on pitch
        in the oppnent area. (excluding the penalty area)

        Args:
            matrix (numpy.ndarray): required matrix
            ax (axes.Axes): axes object.
            kwargs_show: all value to axes.Axes.imshow().
            kwargs_text: all value to axes.Axes.text().
            def_area (bool, optional): plot on defensive area. Defaults to False.
            annotate (bool, optional): to annotate. Defaults to False.

        Returns:
            axes.Axes: axes object
        """
        x_coord = [0, 13.7, 54.22, 68]

        # get required x and y coordinates
        x = [(x, y) for x, y in zip(x_coord[:-1], x_coord[1:])]

        if def_area:
            y = [(34.25, 52), (16.5, 34.25)]
        else:
            y = [(69.75, 87.5), (52, 69.75)]
        
        if annotate:
            matrix_per = np.round(matrix / self.total_touches * 100, 1)

        for index_1, i in enumerate(y):
            for index_2, j in enumerate(x):
                ax.imshow(
                   [[matrix[index_1,index_2]]], extent=[j[0], j[1], i[0], i[1]], **kwargs_show
                )

                if annotate:
                    ax.text(
                        (j[0] + j[1]) / 2, (i[0] + i[1]) / 2,
                        str(matrix_per[index_1, index_2]) + '%', **kwargs_text
                    )

        return ax
    
    def show_halfspace(
        self, matrix, ax, kwargs_show, kwargs_text, annotate=False
    ):
        """
        Function to superimpose a matrix on pitch
        in the oppnent area. (excluding the penalty area)

        Args:
            matrix (numpy.ndarray): required matrix
            ax (axes.Axes): axes object.
            kwargs_show: all value to axes.Axes.imshow().
            kwargs_text: all value to axes.Axes.text().
            annotate (bool, optional): to annotate. Defaults to False.

        Returns:
            axes.Axes: axes object
        """
        x_coord = [0, 13.7, 24.84, 43.16, 54.22, 68]

        # get required x and y coordinates
        x = [(x, y) for x, y in zip(x_coord[:-1], x_coord[1:])]
        y = [(69.75, 87.5), (52, 69.75)]
        
        if annotate:
            matrix_per = np.round(matrix / self.total_touches * 100, 1)

        for index_1, i in enumerate(y):
            for index_2, j in enumerate(x):
                ax.imshow(
                   [[matrix[index_1,index_2]]], extent=[j[0], j[1], i[0], i[1]], **kwargs_show
                )

                if annotate:
                    ax.text(
                        (j[0] + j[1]) / 2, (i[0] + i[1]) / 2,
                        str(matrix_per[index_1, index_2]) + '%', **kwargs_text
                    )

        return ax

    def add_legend(self, ax, legend_color, s, marker, **kwargs):
        """
        Function to add legend

        Args:
            ax (axes.Axes): axes object.
            legend_color (list): of hexcodes.
            s (float): size of the marker.
            marker (str): marker style
            kwargs: all values to axes.Axes.text().
            
        Returns:
            axes.Axes: axes object
        """        
        # scatter points
        x = 6
        for val in legend_color:
            ax.scatter(
                x, -5, s=s, marker=marker, fc=val
            )
            x += 2.2
        
        # annotate legend
        ax.text(
            5.5, -9.4, "low", **kwargs
        )
        ax.text(
            23.8, -9.4, "high", **kwargs
        )
        ax.text(
            15, -9.4, "frequency", **kwargs
        )

        # plot line
        ax.plot(
            [7, 11.4], [-9, -9], color=kwargs["color"], ls=":"
        )
        ax.plot(
            [18.8, 22.4], [-9, -9], color=kwargs["color"], ls=":"
        )

        return ax
