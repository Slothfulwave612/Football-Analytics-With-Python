"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module for shot-maps
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

import my_utils

class ShotMap:
    """
    a wrapper class for creating shot maps.
    """

    def __init__(self, line_color, pitch_color, goal_color, no_goal_color, goal_edge_color):
        """
        <-- constructor -->

        Args:
            line_color (str): line color.
            pitch_color (str): color of the pitch map.
            goal_color (str): color for goal-circle.
            no_goal_color (str): color for no-goal-circle.
            goal_edge_color (str): edge color of the circle.
        """
        self.line_color = line_color
        self.pitch_color = pitch_color
        self.goal_color = goal_color
        self.no_goal_color = no_goal_color
        self.goal_edge_color = goal_edge_color

    def draw_shots(
        self, ax, shot_df, set_alpha=False
    ):
        """
        Function to make the shot map.

        Args:
            ax (axes.Axes): axes object.
            shot_df (pandas.DataFrame): required shot dataframe.
            set_alpha (bool, optional): to set alpha for circles. Defaults to False.
        """
        # traverse the dataframe and plot the shots
        for _, data in shot_df.iterrows():
            # circle size 
            circle_size = (np.sqrt(data["xG"]) * 50)**2
            
            if data["result"] == "Goal":
                fc = self.goal_color
                zorder = 5
            else:
                fc = self.no_goal_color
                zorder = 4
            
            if set_alpha:
                alpha = data["alpha"]
            else:
                alpha = 1
                
            ## creating and adding the required circle
            # circle = plt.Circle(
            #     (data['X'], data['Y']), radius=circle_size,
            #     fc=fc, ec=self.goal_edge_color, zorder=zorder, lw=0.9, alpha=alpha
            # )
            # ax.add_patch(circle)
            ax.scatter(
                data['X'], data['Y'], s=circle_size,
                fc=fc, ec=self.goal_edge_color, zorder=zorder, lw=0.9, alpha=alpha
            )

        return ax

    def draw_shots_(
        self, ax, shot_df, set_alpha=False
    ):
        """
        Function to make the shot map.

        Args:
            ax (axes.Axes): axes object.
            shot_df (pandas.DataFrame): required shot dataframe.
            set_alpha (bool, optional): to set alpha for circles. Defaults to False.
        """
        # traverse the dataframe and plot the shots
        for _, data in shot_df.iterrows():
            # circle size 
            circle_size = (np.sqrt(data["xG"]) * 50)**2
            
            if data["isGoal"] == True:
                fc = self.goal_color
                zorder = 5
            else:
                fc = self.no_goal_color
                zorder = 4
            
            if set_alpha:
                alpha = data["alpha"]
            else:
                alpha = 1
                
            ## creating and adding the required circle
            # circle = plt.Circle(
            #     (data['X'], data['Y']), radius=circle_size,
            #     fc=fc, ec=self.goal_edge_color, zorder=zorder, lw=0.9, alpha=alpha
            # )
            # ax.add_patch(circle)
            ax.scatter(
                data['x'], data['y'], s=circle_size,
                fc=fc, ec=self.goal_edge_color, zorder=zorder, lw=0.9, alpha=alpha
            )

        return ax


    def add_stats(self, ax, shot_df, hex_y=58, hex_size=7000.0, **kwargs):
        """
        Function to add statistics in the shotmap.

        Args:
            ax (axes.Axes): axes object.
            shot_df (pandas.DataFrame): required shot dataframe.
            hex_y (float, optional): y-coordinate for hexagon. Defaults to 58.
            hex_size (float, optional): hexagon size. Defaults to 7000.0
            **kwargs : All other keyword arguments are passed on to matplotlib.axes.Axes.text.
        """
        # compute stats
        xg = round(shot_df["xG"].sum(), 3)
        try:
            # goals = shot_df["result"].value_counts()["Goal"]       
            goals = shot_df["isGoal"].value_counts()[True]     
        except Exception:
            goals = 0
        shots = len(shot_df)                                   
        xg_per_shot = round(xg / shots, 3)

        # text list
        text_list_ax = [
            dict(x=8, y=hex_y - 0.5, s=goals, ha="center", **kwargs),
            dict(x=8, y=50.5, s="Goals", ha="center", **kwargs),
        
            dict(x=32, y=hex_y - 0.5, s=xg, ha="center", **kwargs),
            dict(x=32, y=50.5, s="xG", ha="center", **kwargs),
        
            dict(x=68, y=hex_y - 0.5, s=shots, ha="center", **kwargs),
            dict(x=68, y=50.5, s="Shots", ha="center", **kwargs),
        
            dict(x=92, y=hex_y - 0.5, s=xg_per_shot, ha="center", **kwargs),
            dict(x=92, y=50.5, s="xG/Shot", ha="center", **kwargs),
        ]

        # plot text
        for text in text_list_ax:
            my_utils.plot_text_ax(ax, self.pitch_color, **text)

        # add hexagon
        for x in [8, 32, 68, 92]:
            ax.scatter(
                x=x, y=hex_y, s=hex_size, marker='h', zorder=2,
                ec=self.line_color, fc="none", lw=1.8
            )
        
        return ax

    def add_legend(self, ax, **kwargs):
        """
        Function to add legend.

         Args:
            ax (axes.Axes): axes object.
            **kwargs : All other keyword arguments are passed on to matplotlib.axes.Axes.text.

        Returns:
            figure.Figure: figure object.
            axes.Axes: axes object.
        """
        # text list
        text_list_ax = [
            dict(x=1, y=47.5, s="Outcome:", size=21, **kwargs),
            dict(x=12, y=47.5, s="Goal", size=21, **kwargs),
            dict(x=25, y=47.5, s="No Goal", size=21, **kwargs),
            dict(x=64, y=47.5, s="Low xG", size=21, **kwargs),
            dict(x=100.2, y=47.5, s="High xG", size=21, ha="right", **kwargs)
        ]

        # plot text
        for text in text_list_ax:
            my_utils.plot_text_ax(ax, self.pitch_color, **text)

        # add circle
        self.add_circle(ax, self.goal_color, self.goal_edge_color, self.no_goal_color)

        return ax

    def add_circle(
        self, ax, goal_color, goal_edge_color, no_goal_color
        ):
        """
        Function to plot circles

        Args:
            ax (axes.Axes): axes object.
            goal_color (str): color for goal-circle.
            no_goal_color (str): color for no-goal-circle.
            goal_edge_color (str): edge color of the circle.
        
        Returns:
            figure.Figure: figure object.
            axes.Axes: axes object.
        """
        ax.scatter(
            18.5, 48, s=600, fc=goal_color, ec=goal_edge_color, zorder=3
        )  # for goal
 
        ax.scatter(
            23, 48, s=600, fc=no_goal_color, ec=goal_edge_color, zorder=3
        )  # for shot

        ## to add circle for xG, x_coordinate list
        x_axis = [72, 75, 79, 84, 90]  

        # circle for xG
        for count, i in enumerate(np.linspace(0.05, 1, 5)):
            # radius
            radius = (np.sqrt(i) * 50)**2

            # add marker
            ax.scatter(
                x_axis[count], 48, s=radius, fc=goal_color, ec=goal_edge_color, zorder=3
            )
    
    def add_title(self, fig, text_dict, image=None, **kwargs):
        """
        Args:
            fig (figure.Figure): figure object.
            text_dict (dict): containing text to be plotted.
            image (str): path where image is saved.
            **kwargs : All other keyword arguments are passed on to matplotlib.axes.Axes.text.

        Returns:
            figure.Figure: figure object.
            axes.Axes: axes object.
        """        
        # title list
        text_list_fig = [
            dict(x=0.26, y=0.96, s=text_dict["title"], size=26, **kwargs),
            dict(x=0.26, y=0.935, s=text_dict["sub_title"], size=21, **kwargs),
            dict(x=0.785, y=0.95, s=text_dict["logo"], size=24, ha="right", **kwargs),
        ]

        # plot text
        for text in text_list_fig:
            my_utils.plot_text_fig(fig, self.pitch_color, **text)

        # add image
        if image is not None:
            fig = my_utils.add_image(
                image, fig, 0.165, 0.91, 0.08, 0.08
            )

        return fig
    
    def add_title_(self, fig, text_dict, image=None, **kwargs):
        """
        Args:
            fig (figure.Figure): figure object.
            text_dict (dict): containing text to be plotted.
            image (str): path where image is saved.
            **kwargs : All other keyword arguments are passed on to matplotlib.axes.Axes.text.

        Returns:
            figure.Figure: figure object.
            axes.Axes: axes object.
        """        
        # title list
        text_list_fig = [
            dict(x=0.24, y=0.96, s=text_dict["title"], size=26, **kwargs),
            dict(x=0.24, y=0.935, s=text_dict["sub_title"], size=21, **kwargs),
            dict(x=0.805, y=0.95, s=text_dict["logo"], size=24, ha="right", **kwargs),
        ]

        # plot text
        for text in text_list_fig:
            my_utils.plot_text_fig(fig, self.pitch_color, **text)

        # add image
        if image is not None:
            fig = my_utils.add_image(
                image, fig, 0.145, 0.91, 0.08, 0.08
            )

        return fig
    
    def add_credits(self, fig, text_dict, **kwargs):
        """
        Args:
            fig (axes.Axes): figure object.
            text_dict (dict): containing text to be plotted.
            **kwargs : All other keyword arguments are passed on to matplotlib.axes.Axes.text.

        Returns:
            figure.Figure: figure object.
            axes.Axes: axes object.
        """        
        # title list
        # text_list_fig = [
        #     dict(x=0.78, y=0.01, s=text_dict["credit_right"], size=12, ha="right", **kwargs),
        #     dict(x=0.22, y=0.01, s=text_dict["credit_left"], size=12, **kwargs),
        # ]

        text_list_fig = [
            dict(x=0.783, y=0.01, s=text_dict["credit_right"], size=12, ha="right", **kwargs),
            dict(x=0.218, y=0.01, s=text_dict["credit_left"], size=12, **kwargs),
        ]

        # plot text
        for text in text_list_fig:
            my_utils.plot_text_fig(fig, self.pitch_color, **text)

        return fig
