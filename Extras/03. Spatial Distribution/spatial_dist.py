# -*- coding: utf-8 -*-
"""
Created on Tue May 26 01:24:36 2020

@author: slothfulwave612

Thanks to soccer analytics handbook for the inspiration.

"""
import utility_function_io as ufio
import utility_function_viz as ufvz

## making dataframe for competitions
comp_df = ufio.get_competitions()
4
## picking competition_id = 11 and season_id = 26 from comp df
## La Liga Competition, 2014-15 season
count = 100

for season_id in [37, 38, 39, 40, 41, 21, 22, 23]:
    comp_id = 11
    ## season_id = 1
    
    ## getting match dataframe from our required competiton and season
    match_df = ufio.get_matches(comp_id, season_id)
    
    ## renaming the required columns
    match_df_cols = list(match_df.columns)                  ## making list of the columns
    match_df_cols = ufio.renaming_columns(match_df_cols)    ## new list with renamed columns
    match_df.columns = match_df_cols                        ## renaming the columns
    
    ## storing match_id for each games listed in scoring_df
    match_ids = list(match_df['match_id'].unique())
    
    for match_id in match_ids:
        print('Match {0}: {1}'.format(count, match_id))
        ## combining all events of all matches for a particular season 
        event_df = ufio.make_event_df(match_id=match_id)
        
        ## making dataframe for Lionel Messi
        messi_df = ufio.make_messi_events(event_df)
        
        ## making required matrices
        x_scale = 30
        y_scale = 20
        
        x_bins, y_bins = ufio.make_lists(x_scale, y_scale)
        
        ## making cumulative_actions list 
        player = ufio.cumulative_actions(messi_df, x_scale, y_scale, x_bins, y_bins)
        
        ## making NMF model
        model = ufio.non_neg_matrix_factorization(player)
        
        
        from scipy.ndimage import gaussian_filter
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(20, 12))
        fig, ax = ufvz.createPitch(120, 80, 'yards', 'gray', fig, ax)
          
        z = np.rot90(gaussian_filter(model.components_[0].reshape(x_scale, y_scale), sigma=1.5), 1)
        
        ax.contourf(x_bins, y_bins, z,
                    zorder=2,
                    levels=10,
                    alpha=0.7,
                    cmap='Purples')
        
        fig.savefig('xyz_' + str(count))
        count += 1
        
        plt.close('all')






