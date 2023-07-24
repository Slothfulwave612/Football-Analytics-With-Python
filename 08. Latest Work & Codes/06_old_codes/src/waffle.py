import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data

from mplsoccer import Pitch

import my_utils

def adjustFigAspect(fig,aspect=1):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize,ysize = fig.get_size_inches()
    minsize = min(xsize,ysize)
    xlim = .4*minsize/xsize
    ylim = .4*minsize/ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(left=.5-xlim,
                        right=.5+xlim,
                        bottom=.5-ylim,
                        top=.5+ylim)


def get_coord_list():
    """
    Returns a coordinate list.
    """
    
    start, end = 1, 10

    coord_list = []

    for i in range(start, end+1):
        count = 0
        for j in range(end-i+1, end+1):
            count += 1
            coord_list.append((count, j))

    for i in range(start+1, end+1):
        count = i
        for j in range(start, end+1-i+1):
            coord_list.append((count, j))
            count += 1
    
    return coord_list

def coord_after_rotation(coord_list, angle=np.pi/4.):
    """
    Returns a coordinate list after rotation of the axis.
    """
    for index, coord in enumerate(coord_list):
        x, y = coord
        
        x_new = (x * np.cos(angle)) + (y * np.sin(angle)) 
        y_new = (y * np.cos(angle)) - (x * np.sin(angle)) 

        coord_list[index] = (x_new, y_new)
    
    return coord_list


def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists


def make_waffle(
    nrows, ncols, figsize, total, coord_list, point_list, player_list, facecolor,
    font_normal=None
):
    """
    Function to make waffle charts.
    
    Args:
        nrows, ncols (int): number of rows and number of columns.
        total (int): total players/teams.
        coord_list (list): of coordinates.
        point_list (list): list specifying number of filled circles to be plotted.
        player_list (list): list specifying the player names.
    
    Returns:
        figure.Figure: Figure object.
        axes.Axes: Axes object.
    """
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, facecolor=facecolor, dpi=200)

    adjustFigAspect(fig, 7/8)

    for index, ax in enumerate(fig.get_axes()):
        # set some values    
        ax.set_facecolor(facecolor)
        ax.set_aspect("equal")
        ax.axis("off")
        
        if index == total:
            break

        # init a count
        count = 1
    
        for coord in coord_list:
            # plot the coordinates
            x, y = coord

            if count <= point_list[index]:
                fc, radius, lw, ec = "royalblue", 0.4, 1.5, "#0b4876"

                # pitch.scatter(
                #     x, y, marker='football', s=250, ax=ax, zorder=1.2
                # )

            else:
                fc, radius, lw, ec = "none", 0.3, 1, "#000000"
            
            circle = plt.Circle((x,y), radius=radius, linewidth=lw, fc=fc, ec=ec)
            ax.add_artist(circle)

            count += 1
        
        my_utils.plot_text_ax(
            ax, foreground=facecolor, x=7.9, y=-8.45, s=f"{point_list[index]}%", fontsize=20, 
            ha="center", va="bottom", color="#222222", fontproperties=font_normal.prop
        )
        my_utils.plot_text_ax(
            ax, foreground=facecolor, x=7.9, y=7, s=f"{player_list[index]}", fontsize=20, ha="center", va="bottom", color="#222222",
            fontproperties=font_normal.prop
        )
        ax.set(xlim=(0,15), ylim=(-8.45, 8))
    
    return fig, axes