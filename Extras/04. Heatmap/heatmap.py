# -*- coding: utf-8 -*-
"""
Created on Thu May 28 22:59:16 2020

@author: slothfulwave612

Modules Used(2):-
1. utility_function_io -- Python module for i/o operation.
2. utility_function_viz -- Python module for visualization.
"""
import utility_function_io as ufio
import utility_function_viz as ufvz

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter

def myplot(x, y, s, bins=50):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent

## making dataframe for competitions
comp_df = ufio.get_competitions()

## picking competition_id = 11 and season_id = 22
comp_id = 11
season_id = 26

## getting match dataframe from our required competiton and season
match_df = ufio.get_matches(comp_id, season_id)

## listing all the match ids
match_ids = list(match_df['match_id'].unique())

## getting event for particular match

event_df = ufio.make_event_df(match_id=70273)

## getting events for specified player
player = 'Lionel Andrés Messi Cuccittini'
req_event = ufio.required_events(event_df, player)
req_event['location'].dropna(inplace=True)
'''
## home

x_loc = req_event['location'].apply(lambda x: 120 - x[0])
x_loc = np.array(x_loc)
y_loc = req_event['location'].apply(lambda x: x[1])
y_loc = np.array(y_loc)
'''

## away
x_loc = req_event['location'].apply(lambda x: x[0])
x_loc = np.array(x_loc)
y_loc = req_event['location'].apply(lambda x: x[1])
y_loc = np.array(y_loc)

sigmas = 128

fig, ax = plt.subplots(figsize=(20, 12))

ax = ufvz.createPitch(120, 80, 'black', ax)

fig_2, ax_2 = plt.subplots(figsize=(20, 12))

ax_2 = ufvz.createPitch(120, 80, 'black', ax_2)
ax_2.scatter(x_loc, y_loc)

img, extent = myplot(x_loc, y_loc, sigmas)

ax.imshow(img, extent=[0,120, 0, 80], origin='lower', cmap=cm.jet)
ax.set_xticks([-10,130]) 
ax.set_yticks([-10,90]) 


    














