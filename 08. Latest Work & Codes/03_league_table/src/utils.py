import numpy as np
import pandas as pd

import itertools


def df_for_league_table(df):
    # get home score
    df["home_score"] = df["Score"].apply(lambda x: x.split('–')[0]).astype(int)
    
    # get away score
    df["away_score"] = df["Score"].apply(lambda x: x.split('–')[1]).astype(int)
    
    # make final df
    df = df[["Home", "home_score", "Away", "away_score"]].copy()
    
    return df


def compute_points(x, team):
    home, home_score, away, away_score = x
    diff = home_score - away_score
    w, d, l = 0 , 0, 0
    
    if home == team:
        gf, ga = home_score, away_score
        
        if diff > 0:
            gd, w = 1, 1
            outcome = 'W'
        
        elif diff < 0:
            gd, l = 1, 1
            outcome = 'L'
        
        else:
            gd, d = 0, 1
            outcome = 'D'
        
    elif away == team:
        gf, ga = away_score, home_score
        
        if diff < 0:
            gd, w = -1, 1
            outcome = 'W'
        
        elif diff > 0:
            gd, l = -1, 1
            outcome = 'L'
            
        else:
            gd, d = 0, 1
            outcome = 'D' 

    return w+d+l, w, d, l, gf, ga, diff*gd, 3*w + d, outcome


def swap_rows(df, idx_1, idx_2):
    b, c = df.iloc[idx_1].copy(), df.iloc[idx_2].copy()
    df.iloc[idx_1], df.iloc[idx_2] = c, b
    
    return df


def break_the_tie(df, table, team_1, team_2):
    # fetch the home and away result
    results = df.loc[
        (
            (df["Home"] == team_1) &
            (df["Away"] == team_2)
        ) |
        (
            (df["Home"] == team_2) &
            (df["Away"] == team_1)
        )
    ]
    
    # lambda functions to get score, index and goal-difference
    get_score = lambda team: results.loc[results["Home"] == team, "home_score"].values[0] + results.loc[results["Away"] == team, "away_score"].values[0]
    get_index = lambda team: table.loc[table["team"] == team].index[0]
    get_gd = lambda team: table.loc[table["team"] == team, "goal_diff"].values[0]
    
    # fetch the score
    team_1_score = get_score(team_1)
    team_2_score = get_score(team_2)
    
    # fetch the index
    idx_1, idx_2 =  get_index(team_1), get_index(team_2)
    
    # swap if conditions are True
    if team_1_score > team_2_score and idx_1 > idx_2:
        # check head-to-head
        table = swap_rows(table, idx_1, idx_2)
    
    elif team_2_score > team_1_score and idx_2 > idx_1:
        # check head-to-head
        table = swap_rows(table, idx_2, idx_1)
    
    elif team_1_score == team_2_score:
        # print(team_1, team_2)
        # check goal-difference
        team_1_gd = get_gd(team_1)
        team_2_gd = get_gd(team_2)
        # print(team_1_gd, team_2_gd)
        
        if team_1_gd > team_2_gd and idx_1 > idx_2:
            table = swap_rows(table, idx_1, idx_2)
        elif team_2_gd > team_1_gd and idx_2 > idx_1:
            table = swap_rows(table, idx_2, idx_1)
    
        # print(table)
        # print()

    return table


def make_league_table(df):
    # init empty dict
    league_table = dict()

    # fetch all the teams
    teams = df["Home"].unique()
    
    # iterate and calculate the points
    for team in teams:
        temp_df = df.loc[
            (df["Home"] == team) |
            (df["Away"] == team)
        ]

        # get points, gf, ga & gd
        values = np.array(list(temp_df.apply(lambda x: compute_points(x, team), axis=1).values))
        
        # add the values to dict
        league_table[team] = dict(
            played=sum(map(int, values[:, 0])),
            wins=sum(map(int, values[:, 1])),
            draws=sum(map(int, values[:, 2])),
            lose=sum(map(int, values[:, 3])),
            gf=sum(map(int, values[:, 4])),
            ga=sum(map(int, values[:, 5])),
            goal_diff=sum(map(int, values[:, 6])),
            points=sum(map(int, values[:, 7])),
            last_5 = ''.join(x for x in values[:, 8][-5:][::-1])
        )
    
    # make dataframe
    table = pd.DataFrame(league_table).T

    # set and reset index
    table.index = table.index.set_names(["team"])
    table = table.reset_index()

    # sort the values
    table = table.sort_values(by="points", ascending=False).reset_index(drop=True)
    
    # get the teams that are tied
    for point in table["points"].unique():
        temp_points = table.loc[table["points"] == point]

        if len(temp_points) > 1:
            two_teams = list(
                itertools.permutations(
                    temp_points["team"].unique(), 2
                )
            )
    
            for team_1, team_2 in two_teams:
                table = break_the_tie(df, table, team_1, team_2)
    
    return table