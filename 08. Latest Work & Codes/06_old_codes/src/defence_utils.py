"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module for making defensive vizs.
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy import stats

import Pitch, my_utils

class Defence:
    """
    a wrapper class for plotting defensive actions.
    """

    def __init__(
        self, line_color="#9C9C9C", pitch_color="#222222", orientation="vertical", zorder=3, half=False,
        plot_arrow=False, arrow_color="#F2F2F2", sxy=(20, 16), **kwargs
    ):
        """
        Function to initialize the object of the class.

        Args:
        line_color (str, optional): line color for pitch. Defaults to "#9C9C9C".
        pitch_color (str, optional): pitch color. Defaults to "#222222".
        orientation (str, optional): orientation of the pitch. Defaults to "vertical".
        zorder (int, optional): zorder value.
        half (bool, optional): whether to plot half pitch or not. Defaults to False.
        plot_arrows (bool, optional): to plot the arrow. Defaults to False.
        arrow_color (str, optional): arrow color to be plotted. Defaults to "F2F2F2".
        sxy (tuple, optional): size of the pitch. Defaults to (20,16).
        """    
        self.line_color = line_color
        self.pitch_color = pitch_color
        self.orientation = orientation
        self.zorder = zorder
        self.half = half
        self.plot_arrow = plot_arrow
        self.arrow_color = arrow_color
        self.sxy = sxy
        self.kwargs = kwargs

    def plot_defensive(
        self, df, def_type, **kwargs
    ):
        """
        Function to plot defence maps.

        Args:
            df (pandas.DataFrame): required dataframe.
            def_type (str): type of defensive map to be plotted.
            **kwargs (dict, optional): dict will contain following parameters.
                image_path (str, optional): path of the image.
                orientation_array (list, optional): array defining where the image will be plotted. e.g. to [0.14, 0.629, 0.1, 0.03].
                main_title (str, optional): title of the plot.
                sub_title (str, optional): sub-title of the plot.
                credit (str): credit at the end. Defaults to None.
                main_coord (tuple, optional): coordinates for main title. Defaults to e.g. (9, 109.5).
                sub_coord (tuple, optional): coordinates for sub title. Defaults to e.g. (9, 107).
                credit_coord (tuple, optional): coordinates for credits. Defaults to e.g. (68, 50.5).
                save_path (str, optional): path where image will be saved. 
                figax (tuple, optional): contains fig and axes object. 

        Returns:
            pyplot.Figure: figure object.
            axes.Axes: axes object.
        """    
        ## init object of Pitch class
        pitch = Pitch.Pitch(line_color=self.line_color, pitch_color=self.pitch_color, orientation=self.orientation, half=self.half)

        ## plot pitch
        if kwargs.get("figax"):
            fig, ax = pitch.create_pitch(figax=kwargs["figax"])
        else:
            fig, ax = pitch.create_pitch()

        if def_type == "all_def_activity":
            ax = self.all_def_activity(df, ax)
        
        return fig, ax

    def all_def_activity(
        self, df, ax, **kwargs
    ):
      """
        Function to plot all the passes.

        Args:
            df (pandas.DataFrame): required dataframe.
            ax (Axes.axes): axes object.
            arrow (Arrows.Arrow): object of Arrow class.
            
        Returns:
            axes.Axes: axes object.
      """ 
      ## traverse the dataframe
      for _, data in df.iterrows():
          ## fetch start and end location, 68 minus for inverting axis for verical plot
        x, y = data['x'], data['y']

        ## fetch color
        if data["outcomeType_displayName"] == "Successful":
            color = self.kwargs["succ_color"]
        elif data["outcomeType_displayName"] == "Unsuccessful":
            color = self.kwargs["unsucc_color"]
        else:
            raise ValueError("Orientation not understood")
            
        ## plot markers
        if data["type_displayName"] == "Aerial":
            ax.scatter(
                x, y, s=self.kwargs["scatter_size"], color=color, marker="^", zorder=self.zorder
            )
        
        elif data["type_displayName"] == "Tackle":
            ax.scatter(
                x, y, s=self.kwargs["scatter_size"], color=color, marker="v", zorder=self.zorder
            )

        elif data["type_displayName"] == "Challenge":
            ax.scatter(
                x, y, s=self.kwargs["scatter_size"], color=color, marker="*", zorder=self.zorder
            )
        
        elif data["type_displayName"] == "Clearance":
            ax.scatter(
                x, y, s=self.kwargs["scatter_size"], color=color, marker="2", zorder=self.zorder
            )
        
        elif data["type_displayName"] == "Interception":
            ax.scatter(
                x, y, s=self.kwargs["scatter_size"], color=color, marker="o", zorder=self.zorder
            )

        elif data["type_displayName"] == "BlockedPass":
            ax.scatter(
                x, y, s=self.kwargs["scatter_size"], color=color, marker="X", zorder=self.zorder
            )

        elif data["type_displayName"] == "Foul":
            ax.scatter(
                x, y, s=self.kwargs["scatter_size"], color="#9F9F9F", marker="$f$", zorder=self.zorder
            )

      return ax
        

    def defensive_activity(
        self, df, divide_pitch=False
    ):
        ## init the object of the Pitch class and plot the pitch
        pitch = Pitch.Pitch(line_color=self.line_color, pitch_color=self.pitch_color, orientation=self.orientation)
        fig, ax = pitch.create_pitch()

        ## divide pitch into 6 parts
        if divide_pitch == True:
            if self.orientation == "horizontal":
                ax.plot([16.5, 16.5], [0, 68], color=self.line_color, zorder=self.zorder)
                ax.plot([34.25, 34.25], [0, 68], color=self.line_color, zorder=self.zorder)
                ax.plot([69.75, 69.75], [0, 68], color=self.line_color, zorder=self.zorder)
                ax.plot([87.5, 87.5], [0, 68], color=self.line_color, zorder=self.zorder)
            elif self.orientation == "vertical":
                ax.plot([0, 68], [16.5, 16.5], color=self.line_color, zorder=self.zorder)
                ax.plot([0, 68], [34.25, 34.25], color=self.line_color, zorder=self.zorder)
                ax.plot([0, 68], [69.75, 69.75], color=self.line_color, zorder=self.zorder)
                ax.plot([0, 68], [87.5, 87.5], color=self.line_color, zorder=self.zorder)

        ## plot all the defensive activities
        ax.scatter(df['x'], df['y'], s=self.kwargs["scatter_size"], color=self.kwargs["scatter_color"])

        return fig, ax

    def get_ppda_zone_values(self, df, team_name):
        """
        Function to get PPDA values for each zones.

        Args:
            df (pandas.DataFrame): containing event data.
            team_name (str): name of the team in consideration.

        Returns:
            list: containing PPDA values for each zones
        """        
        ## init zone-value list
        x_coord = [
            0, 16.5, 34.25, 52, 69.75, 87.5, 104
        ]

        ## init empty list
        ppda_values = []

        for i in range(0, len(x_coord) - 1):
            ## total passes by the opponent
            opp_pass = df.loc[
                (df['x'] >= x_coord[i]) & 
                (df['x'] < x_coord[i+1]) & 
                (df["team_name"] != team_name) &
                (df["type_displayName"] == "Pass")
            ].shape[0]

            ## defensive activities
            team_def = df.loc[
                (df['x'] >= x_coord[i]) & 
                (df['x'] < x_coord[i+1]) & 
                (df["team_name"] == team_name) &
                (df["type_displayName"].isin(
                    ["Interception", "Challenge", "Tackle", "Foul"]
                ))
            ].shape[0]

            ## ppda value
            ppda_values.append(
                opp_pass / team_def
            )

        return ppda_values

    def get_ppda_values(
        self, competition_id, season_id
    ):
        """
        Function to get ppda values for all teams in a season.

        Args:
            competition_id (int): competition id.
            season_id (int): season id.
        
        Returns:
            numpy.ndarray: array containing ppda values.
            list: of team names
        """    
        ## path to match file
        path = f"../data/matches/{season_id}/{competition_id}.json"

        ## get matches
        match_df = my_utils.get_matches(path)

        ## fetch the name of the teams
        teams = sorted(
            match_df["home_team_name"].unique()
        )

        ## init empty array 
        ppda_array = np.array([])

        ## iterate through team list
        for team in teams:
            ## fetch match-ids
            match_ids = match_df.loc[
                (match_df["home_team_name"] == team) |
                (match_df["away_team_name"] == team), "match_id"
            ].values
            
            ## make event data frame for all the matches
            event_df = my_utils.load_team_season(match_ids)
            
            ## get ppda values
            ppda_zones = self.get_ppda_zone_values(event_df, team)           

            ## append to ppda-array
            ppda_array = np.append(ppda_array, ppda_zones)

        ## reshape the array
        ppda_array = ppda_array.reshape(
            len(teams), 6
        )

        return ppda_array, teams
    
    def make_ppda_charts(
        self, competition_id, season_id, nrows, ncols, figsize, team_name_color, cmap="Blues",
        ppda_values=None, teams=None, **kwargs
    ):
        """
        Function to make PPDA charts.

        Args:
            competition_id (int): competition id.
            season_id (int): season id.
            nrows (int): number of rows.
            ncols (int): number of columns.
            figsize (tuple): size of the figure.
            team_name_color (str): color code for the team-name displayed above the plot.
            cmap (str, optional): color-map for PPDA charts. Defaults to "Blues".
            **kwargs: for text
        
        Returns:
            pyplot.Figure: figure object.
            axes.Axes: axes object.
        """    
        if type(cmap) == list:
            cmap = colors.ListedColormap(cmap)

        ## calculate ppda values and their corresponding team names
        if ppda_values is None:
            ppda_values, teams = self.get_ppda_values(competition_id, season_id)

        ## normalize ppda_values (using z-score)
        for i in range(len(ppda_values[0])):
            # print(stats.zscore(ppda_values[:, i]))
            ppda_values[:, i] = -stats.zscore(ppda_values[:, i])

        ## make subplots
        fig, ax = plt.subplots(
            nrows=nrows, ncols=ncols, facecolor=self.pitch_color,
            figsize=figsize
        )

        ## make default Pitch map
        pitch = Pitch.Pitch(
            line_color=self.line_color, pitch_color=self.pitch_color,
            orientation=self.orientation, half=self.half, plot_arrow=self.plot_arrow,
            arrow_color=self.arrow_color, sxy=self.sxy
        )

        ## init counter
        counter = 0

        for axes in fig.get_axes():
            ## create pitchmap
            fig, axes = pitch.create_pitch(zorder_line=5, figax=(fig, axes))

            ## plotting heatmap
            axes.imshow(
                np.zeros((3,1)) + ppda_values[counter, 0], zorder=2, aspect="auto", vmin=-1.5, vmax=1.5, 
                extent=(0, 16.5, 0, 68), cmap=cmap
            )
            axes.imshow(
                np.zeros((3,1)) + ppda_values[counter, 1], zorder=2, aspect="auto", vmin=-1.5, vmax=1.5, 
                extent=(16.51, 34.25, 0, 68), cmap=cmap
            )
            axes.imshow(
                np.zeros((3,1)) + ppda_values[counter, 2], zorder=2, aspect="auto", vmin=-1.5, vmax=1.5, 
                extent=(34.251, 52.0, 0, 68), cmap=cmap
            )
            axes.imshow(
                np.zeros((3,1)) + ppda_values[counter, 3], zorder=2, aspect="auto", vmin=-1.5, vmax=1.5, 
                extent=(52.01, 69.75, 0, 68), cmap=cmap
            )
            axes.imshow(
                np.zeros((3,1)) + ppda_values[counter, 4], zorder=2, aspect="auto", vmin=-1.5, vmax=1.5, 
                extent=(69.751, 87.5, 0, 68), cmap=cmap
            )
            axes.imshow(
                np.zeros((3,1)) + ppda_values[counter, 5], zorder=2, aspect="auto", vmin=-1.5, vmax=1.5, 
                extent=(87.51, 104, 0, 68), cmap=cmap
            )

            ## set title
            axes.set_title(
                teams[counter], zorder=4, color=team_name_color, **kwargs
            )

            ## tidy axis
            axes.axis("off")

            ## set axis limits
            axes.set(xlim=(0,104), ylim=(0,68))

            ## increment the counter
            counter += 1
        
        ## tight layout
        plt.tight_layout(pad=4.0)

        ## add colorbar
        fraction = 0.013
        norm = mpl.colors.Normalize(vmin=-1.5, vmax=1.5)
        axes.figure.colorbar(
            mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
            ax=ax, pad=0.023, fraction=fraction
        )

        return fig, ax