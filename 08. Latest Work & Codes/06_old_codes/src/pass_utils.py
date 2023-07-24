"""
__author__: Anmol_Durgapal(@slothfulwave612)

Python module to implement all passes functions.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import my_utils

def passes_into_pen(x):
    start_x, start_y, end_x, end_y = x

    if (87.5 <= end_x <= 104) & (13.84 <= end_y <= 54.16):
        if (((0 <= start_x <= 87.5) & (0 <= start_y <= 68)) | \
            ((87.5 < start_x <= 104)) & \
                ((0 <= start_y <= 13.84) | (54.16 <= start_y <= 68))):
            return True
    return False

def progressive_passes(x):
    start_x, end_x = x

    # from wyscout glossary
    if start_x <= 52.0 and end_x <= 52.0:
        # team's half
        if end_x - start_x >= 30.0:
            return True
        
    elif start_x <= 52.0 and end_x > 52.0:
        # team's half --> opponent's half
        if end_x - start_x >= 15:
            return True

    elif start_x > 52.0 and end_x > 52.0:
        # opponent's half
        if end_x - start_x >= 10:
            return True
    
    return False

# class Pass:
#     """
#     a wrapper class for pass methods.
#     """

#     def __init__(
#         self, line_color="#9C9C9C", pitch_color="#222222", orientation="vertical", half=False,
#         arrow_type="cirtri", opp_half=False, **kwargs
#     ):
#         """
#         Function to initialize the object of the class.

#         Args:
#         line_color (str, optional): line color for pitch. Defaults to "#9C9C9C".
#         pitch_color (str, optional): pitch color. Defaults to "#222222".
#         orientation (str, optional): orientation of the pitch. Defaults to "vertical".
#         half (bool, optional): whether to plot half pitch or not. Defaults to False.
#         arrow_type (str, optional): type of arrow to be plotted. Defaults to "cirtri".
#         opp_half (bool, optional): to only plot in opposition half or not. Defaults to False.
#         """    
#         self.line_color = line_color
#         self.pitch_color = pitch_color
#         self.orientation = orientation
#         self.half = half
#         self.arrow_type = arrow_type
#         self.opp_half = opp_half
#         self.kwargs = kwargs

#     def plot_passes(
#         self, df, pass_type, **kwargs
#     ):
#         """
#         Function to plot all the passes.

#         Args:
#             df (pandas.DataFrame): required dataframe.
#             pass_type (str): type of pass map to be plotted.
#             **kwargs (dict, optional): dict will contain following parameters.
#                 image_path (str, optional): path of the image.
#                 orientation_array (list, optional): array defining where the image will be plotted. e.g. to [0.14, 0.629, 0.1, 0.03].
#                 main_title (str, optional): title of the plot.
#                 sub_title (str, optional): sub-title of the plot.
#                 credit (str): credit at the end. Defaults to None.
#                 main_coord (tuple, optional): coordinates for main title. Defaults to e.g. (9, 109.5).
#                 sub_coord (tuple, optional): coordinates for sub title. Defaults to e.g. (9, 107).
#                 credit_coord (tuple, optional): coordinates for credits. Defaults to e.g. (68, 50.5).
#                 save_path (str, optional): path where image will be saved.
#                 dpi (int, optional) : dot per inches.
#                 figax (tuple, optional): contains fig and axes object. 

#         Returns:
#             pyplot.Figure: figure object.
#             axes.Axes: axes object.
#         """    
#         ## init object of Pitch class
#         pitch = Pitch.Pitch(line_color=self.line_color, pitch_color=self.pitch_color, orientation=self.orientation, half=self.half)

#         ## plot pitch
#         if kwargs.get("figax"):
#             fig, ax = pitch.create_pitch(figax=kwargs["figax"])
#         else:
#             fig, ax = pitch.create_pitch()

#         ## init object of Arrow class   
#         arrow = Arrows.Arrow(arrow_type=self.arrow_type)

#         if pass_type == "all_passes":
#             ## plot all passes
#             ax =  self.all_passes(df, ax, arrow, **kwargs)

#         elif pass_type == "passes_into_pen":
#             ## plot passes into penalty area
#             ax =  self.passes_into_pen(df, ax, arrow, **kwargs)

#         elif pass_type == "progressive_passes":
#             ## plot progressive passes
#             ax = self.make_progressive_map(df, ax, arrow, **kwargs)

#         elif pass_type == "deep_completion":
#             ## plot deep completion
#             ax =  self.deep_completion(df, ax, arrow, **kwargs)
#         else:
#             raise ValueError("Pass type not understood")

#         ## add image to the figure
#         if kwargs.get("image_path"):
#             fig = my_utils.add_image(
#                 kwargs["image_path"], fig, kwargs["orientation_array"][0],
#                 kwargs["orientation_array"][1], kwargs["orientation_array"][2],
#                 kwargs["orientation_array"][3]
#             )

#         ## plot title
#         if kwargs.get("main_coord") and kwargs.get("main_title"):
#             ax.text(
#                 kwargs["main_coord"][0], kwargs["main_coord"][1], kwargs["main_title"],
#                 fontsize=kwargs["main_size"], fontweight="bold", color="#ececec", fontfamily=kwargs["font"]
#             )

#         ## plot sub-title
#         if kwargs.get("sub_coord") and kwargs.get("sub_title"):
#             ax.text(
#                 kwargs["sub_coord"][0], kwargs["sub_coord"][1], kwargs["sub_title"],
#                 fontsize=kwargs["sub_size"], fontweight="bold", color="#ececec", fontfamily=kwargs["font"]
#             )

#         ## add credits
#         if kwargs.get("credit_coord") and kwargs.get("credit"):
#             ax.text(
#                 kwargs["credit_coord"][0], kwargs["credit_coord"][1], kwargs["credit"],  
#                 fontsize=kwargs["credit_size"], color="#ececec", fontstyle="italic", fontfamily="Liberation Serif", ha="right", va="center"
#             )

#         ## set axis
#         if self.orientation == "vertical" and self.half==True:
#             ax.set(xlim=(-2,70), ylim=(48, 112))
#         elif self.orientation == "vertical":
#             ax.set(xlim=(-2,70), ylim=(-2, 112))
#         elif self.orientation == "horizontal":
#             ax.set_xticks([-1, 105])
#             ax.set_yticks([-1, 73])

#         if kwargs.get("save_path"):
#             ## save image
#             fig.savefig(kwargs["save_path"], dpi=kwargs["dpi"], bbox_inches="tight")

#         return fig, ax


#     def all_passes(
#         self, df, ax, arrow, **kwargs
#     ):
#         """
#         Function to plot all the passes.

#         Args:
#             df (pandas.DataFrame): required dataframe.
#             ax (Axes.axes): axes object.
#             arrow (Arrows.Arrow): object of Arrow class.
            
#         Returns:
#             axes.Axes: axes object.
#         """    
#         ## init two variables
#         success, unsuccess = 0, 0

#         if self.opp_half == True:
#             temp_x = 52.0
#         else:
#             temp_x = 0

#         ## traverse the dataframe
#         for _, data in df.iterrows():
#             start_x, start_y = data['x'], data['y']
#             end_x, end_y = data["endX"], data["endY"]

#             if start_x >= temp_x and end_x >= temp_x:
#                 if data["outcomeType_displayName"] == "Successful":

#                     if self.arrow_type == "cirtri":
#                         ax = arrow.plot_arrow(
#                             ax, start_x, start_y, end_x, end_y,
#                             radius=self.kwargs["radius"], circle_fc=self.kwargs["circle_fc"], circle_alpha=self.kwargs["circle_alpha"],
#                             circle_ec=self.kwargs["circle_ec"], tri_fc=self.kwargs["tri_fc"], tri_alpha=self.kwargs["tri_alpha"], zorder=7
#                         )
#                     elif self.arrow_type == "simple_arrows":
#                         ax = arrow.plot_arrow(
#                             ax, start_x, start_y, end_x, end_y, color=self.kwargs["color"],
#                             headlength=self.kwargs["headlength"], headwidth=self.kwargs["headwidth"],
#                             alpha=self.kwargs["alpha"]
#                         )

#                     success += 1

#                 elif data["outcomeType_displayName"] == "Unsuccessful":

#                     if self.arrow_type == "cirtri":
#                         ax = arrow.plot_arrow(
#                             ax, start_x, start_y, end_x, end_y,
#                             radius=self.kwargs["radius"], circle_fc=self.kwargs["circle_fc_uns"], circle_alpha=self.kwargs["circle_alpha_uns"],
#                             circle_ec=self.kwargs["circle_ec_uns"], tri_fc=self.kwargs["tri_fc_uns"], tri_alpha=self.kwargs["tri_alpha_uns"], 
#                             plot_first="triangle", zorder=6
#                         )
#                     elif self.arrow_type == "simple_arrows":
#                         ax = arrow.plot_arrow(
#                             ax, start_x, start_y, end_x, end_y, color=self.kwargs["color_uns"],
#                             headlength=self.kwargs["headlength"], headwidth=self.kwargs["headwidth"]
#                         )
#                     unsuccess += 1
        
#         return ax
    
#     def passes_into_pen(
#         self, df, ax, arrow, **kwargs
#     ):
#         """
#         Function to plot all the passes that went into the penalty box.

#         Args:
#             df (pandas.DataFrame): required dataframe.
#             ax (Axes.axes): axes object.
#             arrow (Arrows.Arrow): object of Arrow class.

#         Returns:
#             axes.Axes: axes object.
#         """   
#         ## traverse the dataframe
#         for _, data in df.iterrows():
#             start_x, start_y = data['x'], data['y']
#             end_x, end_y = data["endX"], data["endY"]

#             if ((87.5 <= start_x <= 104) and (start_y <= 13.84 or start_y >= 54.16)) or \
#                 (52.0 <= start_x <= 87.5 and  0 <= start_y <= 68):

#                 if end_x >= 87.5 and 13.84 <= end_y <= 54.16:
#                     if data["outcomeType_displayName"] == "Successful":
#                         ax = arrow.plot_arrow(
#                             ax, start_x, start_y, end_x, end_y,
#                             radius=self.kwargs["radius"], circle_fc=self.kwargs["circle_fc"], circle_alpha=self.kwargs["circle_alpha"],
#                             circle_ec=self.kwargs["circle_ec"], tri_fc=self.kwargs["tri_fc"], tri_alpha=self.kwargs["tri_alpha"],
#                             zorder=5
#                         )

#                     # elif data["outcomeType_displayName"] == "Unsuccessful":
#                     #     ax = arrow.plot_arrow(
#                     #         ax, start_x, start_y, end_x, end_y,
#                     #         radius=0.8, circle_fc="#121212", circle_alpha=0.8,
#                     #         circle_ec="#9F9F9F", tri_fc="#9F9F9F", tri_alpha=0.7, plot_first="triangle", zorder=4
#                     #     )

#         return ax
    
#     def make_progressive_map(
#         self, df, ax, arrow, **kwargs
#     ):
#         """
#         Function for making progressive pass map.

#         Args:
#             df (pandas.DataFrame): required dataframe.
#             ax (Axes.axes): axes object.
#             arrow (Arrows.Arrow): object of Arrow class.

#         Returns:
#             axes.Axes: axes object.
#         """    
#         # if self.orientation == "vertical":
#         #     goal_coord = (34, 104)
#         # elif self.orientation == "horizontal":
#         #     goal_coord = (104, 34)
#         # else:
#         #     raise ValueError("Orientation not understood")

#         ## traverse the dataframe
#         for _, data in df.iterrows():
#             ## fetch the start and end coordinates
#             x_start, y_start = data['x'], data['y']
#             x_end, y_end = data['endX'], data['endY']

#             ## init a variable to_plot as False
#             to_plot = False

#             if self.orientation == "horizontal":
#                 ## if there is a complete pass in the penalty box
#                 ## ADD HERE 
#                 if x_end >= 87.5 and 13.84 <= y_end <= 54.16:
#                     to_plot = True
                
#                 ## from wyscout glossary
#                 elif x_start <= 52.0 and x_end <= 52.0:
#                     ## team's half
#                     if x_end - x_start >= 30.0:
#                         to_plot = True
                    
#                 elif x_start <= 52.0 and x_end > 52.0:
#                     ## team's half --> opponent's half
#                     if x_end - x_start >= 15:
#                         to_plot = True

#                 elif x_start > 52.0 and x_end > 52.0:
#                     ## opponent's half
#                     if x_end - x_start >= 10:
#                         to_plot = True     

#             elif self.orientation == "vertical":
#                 ## if there is a complete pass in the penalty box
#                 if ((87.5 <= y_start <= 104) and (x_start <= 13.84 or x_start >= 54.16)) or \
#                 (52.0 <= x_start <= 87.5 and  0 <= x_start <= 68):
#                     if y_end >= 87.5 and 13.84 <= x_end <= 54.16:
#                         to_plot = True
            
#                 ## from wyscout glossary
#                 if y_start <= 52.0 and y_end <= 52.0:
#                     ## team's half
#                     if y_end - y_start >= 30.0:
#                         to_plot = True
                    
#                 elif y_start <= 52.0 and y_end > 52.0:
#                     ## team's half --> opponent's half
#                     if y_end - y_start >= 15:
#                         to_plot = True

#                 elif y_start > 52.0 and y_end > 52.0:
#                     ## opponent's half
#                     if y_end - y_start >= 10:
#                         to_plot = True     

#             # if my_utils.disance_sqr((x_start, y_start), goal_coord) * 0.75**2 >= my_utils.disance_sqr((x_end, y_end), goal_coord):

#             ## plot arrows
#             if to_plot == True:
#                 if self.arrow_type == "simple_arrows":
#                     ax = arrow.plot_arrow(
#                         ax, x_start, y_start, x_end, y_end, color=self.kwargs["color"],
#                         headlength=self.kwargs["headlength"], headwidth=self.kwargs["headwidth"]
#                     )
                
#                 elif self.arrow_type == "cirtri":
#                     ax = arrow.plot_arrow(
#                         ax, x_start, y_start, x_end, y_end,
#                         radius=self.kwargs["radius"], circle_fc=self.kwargs["circle_fc"], circle_alpha=self.kwargs["circle_alpha"],
#                         circle_ec=self.kwargs["circle_ec"], tri_fc=self.kwargs["tri_fc"], tri_alpha=self.kwargs["tri_alpha"], zorder=5
#                     )
        
#         return ax

#     def deep_completion(
#         self, df, ax, arrow, **kwargs
#     ):
#         """
#         Function for making deep completion pass map.

#         Args:
#             df (pandas.DataFrame): required dataframe.
#             ax (Axes.axes): axes object.
#             arrow (Arrows.Arrow): object of Arrow class.

#         Returns:
#             axes.Axes: axes object.
#         """    

#         ## UPDATE HERE

#         if self.orientation == "vertical":
#             goal_coord = (34, 104)
#         elif self.orientation == "horizontal":
#             goal_coord = (104, 34)
#         else:
#             raise ValueError("Orientation not understood")

#         ## traverse the dataframe
#         for _, data in df.iterrows():
#             ## fetch the start and end coordinates
#             x_start, y_start = data['x'], data['y']
#             x_end, y_end = data["endX"], data["endY"]

#             distance_from_goal = np.sqrt(
#                 my_utils.disance_sqr(goal_coord, (x_end, y_end))
#             )

#             if distance_from_goal <= 20:
#                 ## plot arrows
#                 if self.arrow_type == "simple_arrows":
#                     ax = arrow.plot_arrow(
#                         ax, x_start, y_start, x_end, y_end, color=self.kwargs["color"],
#                         headlength=self.kwargs["headlength"], headwidth=self.kwargs["headwidth"]
#                     )
                
#                 elif self.arrow_type == "cirtri":
#                     ax = arrow.plot_arrow(
#                         ax, x_start, y_start, x_end, y_end,
#                         radius=self.kwargs["radius"], circle_fc=self.kwargs["circle_fc"], circle_alpha=self.kwargs["circle_alpha"],
#                         circle_ec=self.kwargs["circle_ec"], tri_fc=self.kwargs["tri_fc"], tri_alpha=self.kwargs["tri_alpha"]
#                     )

#         return ax
