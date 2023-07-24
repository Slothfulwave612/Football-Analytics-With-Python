"""
author : Anmol Durgapal (@slothfulwave612)

Python module containing utility functions for visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from mplsoccer import add_image
from PIL import Image


def adjustFigAspect(fig,aspect=1):
    """
    Adjust the subplot parameters so that 
    the figure has the correct aspect ratio.
    """
    xsize,ysize = fig.get_size_inches()

    minsize = min(xsize,ysize)

    xlim = .4*minsize/xsize
    ylim = .4*minsize/ysize

    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect

    fig.subplots_adjust(
        left=.5-xlim, right=.5+xlim,
        bottom=.5-ylim, top=.5+ylim
    )


def make_static_viz(
    df, month_dict, background_color, 
    player_in_focus, color_player, color_others,
    figsize, dpi_plot=100, aspect_ratio=1, 
    label_size=8, label_color="#303030",
    font_normal=None, font_bold=None,
    width=2, image=None
):
    """
    Function to create static trendline-chart.

    Parameters
    ----------
    df : pandas.DataFrame
        Containing goals scored per month.
    month_dict : dict
        key --> month-number & value --> month-name.
    background_color : str
        The background color of the plot.
    player_in_focus : str
        Player's name.
    color_player : str
        Color for player to be highlighted.
    color_others : str
        Color for other players.
    figsize : sequence of floats.
        The length and width of the plot.
    dpi_plot : int, defaults 100
        The dpi for the plot.
    aspect_ratio : float, defaults 1
        The aspect ratio for the plot.
    

    Returns
    -------
    figure.Figure : figure object.
    axes.Axes : axes object.
    """
    # create subplot
    fig, ax = plt.subplots(
        figsize=figsize, dpi=dpi_plot,
        facecolor=background_color,
    )

    # set color for axes
    ax.set_facecolor(background_color)

    # adjust by aspect ratio
    adjustFigAspect(fig,aspect=aspect_ratio)

    index = len(player_in_focus) - 1

    # traverse and plot
    for player in df.columns[::-1]:
        if player in player_in_focus:
            color = color_player[index]
            zorder = 3
            fp = font_bold.prop
            alpha = 1
            lw = 1.5
            index -= 1
        else:
            color = color_others
            zorder = 2
            fp = font_normal.prop
            alpha = 0.5
            lw = 1

        months = month_dict.values()

        ax.plot(
            months, df[player][month_dict.keys()], color=color, 
            zorder=zorder, alpha=alpha, lw=lw,
        )

        ax.text(
            len(month_dict) - 1 + 0.03, df[player].values[-1],
            s=player + ' (' + str(int(df[player].values[-1])) + ')',
            color=color, zorder=zorder, fontproperties=fp,
            va="center", size=label_size+1,
            path_effects=[
                path_effects.withStroke(linewidth=width, foreground=background_color)
            ],
        )
        
    # set axis limit
    ax.set(xlim=(0,8.1), ylim=(0, 25.5))

    # left-align xticklables
    ax.set_xticklabels(
        labels=month_dict.values(), ha="left",
    )

    # show ticks on right y-axis
    ax.yaxis.tick_right()

    for label in ax.get_xticklabels():
        label.set_fontproperties(font_normal.prop)
        label.set_size(label_size)
    
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_normal.prop)
        label.set_size(label_size)
        label.set_color(label_color)

    # hide the spines
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # color bottom spine
    ax.spines["bottom"].set_color(label_color)

    # color ticks
    ax.tick_params(axis="x", colors=label_color)
    ax.tick_params(axis='y',which='major',color="none")

    # grid
    ax.grid(b=True, axis='y', alpha=0.5, zorder=0)

    # add image
    if image is not None:
        image = Image.open(image)
        _ = add_image(image, fig, 0.709, 0.716, 0.025, 0.025)

    return fig, ax
