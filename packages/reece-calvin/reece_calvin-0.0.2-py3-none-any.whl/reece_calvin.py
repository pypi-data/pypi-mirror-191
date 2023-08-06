#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 09:04:18 2023

@author: reececalvin
"""

from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

def rf_clf(dfs, feature_lists, y_val, plt_max_depth = 30):
    '''

    Parameters
    ----------
    dfs : pandas dataframe
    feature_lists : list of strings
        Each string in the list has to be a column in dfs.
    y_val : string
        Target variable.
    plt_max_depth : INT, optional
        Max depth of the classifier. The default is 30.

    Returns
    -------
    models : TYPE
        DESCRIPTION.

    '''
    
    models = []
    
    for df,feature_list in zip(dfs, feature_lists):
        
        max_depth = plt_max_depth

        x_feat_list = feature_list

        df_standard = df[x_feat_list]/df[x_feat_list].std()

        df_standard[y_val] = df[y_val]

        sample = df_standard.sample(frac=.25)

        # extract data from dataframe
        x = sample.loc[:, x_feat_list].values
        y = sample.loc[:, y_val].values

        rf_clf = RandomForestClassifier(max_depth=max_depth, n_estimators=100)

        rf_clf.fit(x, y)

        sns.set()

        plot_feat_import(x_feat_list, rf_clf.feature_importances_)

        training_df = df_standard.sample(frac=0.3)

        # The remaining data is the testing data
        testing_df = df_standard.drop(training_df.index)


        X = training_df[x_feat_list]
        Y = training_df[y_val]

        x = testing_df[x_feat_list]
        y_true = testing_df[y_val]

        ac_scores = {}
        best_depth = 0
        best_ac = 0
        
        for depth in range(10,70,5):
            rf_clf = RandomForestClassifier(max_depth=max_depth, n_estimators=100)
            rf_clf.fit(X, Y)
            y_pred = rf_clf.predict(x)

            ac_score = metrics.accuracy_score(y_true, y_pred)

            ac_scores[depth] = ac_score
            
            if ac_score > best_ac:
                best_depth = depth
            
        rf_clf = RandomForestClassifier(max_depth=best_depth, n_estimators=100)
        rf_clf.fit(X, Y)
        
        models.append((rf_clf, ac_scores))
        
    return models

def plot_feat_import(feat_list, feat_import, sort=True, limit=None):
    """ plots feature importances in a horizontal bar chart
    
    Args:
        feat_list (list): str names of features
        feat_import (np.array): feature importances (mean gini reduce)
        sort (bool): if True, sorts features in decreasing importance
            from top to bottom of plot
        limit (int): if passed, limits the number of features shown
            to this value    
    """
    
    if sort:
        # sort features in decreasing importance
        idx = np.argsort(feat_import).astype(int)
        feat_list = [feat_list[_idx] for _idx in idx]
        feat_import = feat_import[idx] 
        
    if limit is not None:
        # limit to the first limit feature
        feat_list = feat_list[:limit]
        feat_import = feat_import[:limit]
    
    # plot and label feature importance
    plt.barh(feat_list, feat_import)
    plt.gcf().set_size_inches(5, len(feat_list) / 2)
    plt.xlabel('Feature importance\n(Mean decrease in Gini across all Decision Trees)')
    
def inning_game_ids(pxp):
    """
    Categorize plays based on game names and innings
    
    pxp: DataFrame
        DataFrame of play by play data
        
    Returns:
        DataFrame of categorized plays with game_id and inning_id columns
    """
    plays = []
    game_id = 0
    inning_id = 0
    game = None
    inning = None
    
    for play in pxp.to_dict('records'):
        current_game = play.get('Notes')
        current_inning = play.get('Inning')
        
        if current_game != game:
            game_id += 1
            inning_id += 1
            game = current_game
            inning = current_inning
        elif current_inning != inning:
            inning_id += 1
            inning = current_inning
        
        play['game_id'] = game_id
        play['inning_id'] = inning_id
        plays.append(play)
    
    return pd.DataFrame(plays)

def base_count_score(pxp):
    """
    Process play-by-play data by splitting scores, counts, and runners on base
    
    pxp: DataFrame
        DataFrame of play by play data
        
    Returns:
        DataFrame of processed play-by-play data with added columns for bat_score, 
        balls, strikes, on_1b, on_2b, and on_3b
    """
    data = pxp.to_dict('records')
    
    for play in data:
        score = play['Score'].split('-')
        if play['Inning'][0] == 'T':
            play['bat_score'] = int(score[0])
        else:
            play['bat_score'] = int(score[1])
        
        count = play['Count'].split('-')
        play['balls'] = count[0]
        play['strikes'] = count[1]
        
        play['on_1b'] = 1 if '1B' in play['Runners On Base'] else 0
        play['on_2b'] = 1 if '2B' in play['Runners On Base'] else 0
        play['on_3b'] = 1 if '3B' in play['Runners On Base'] else 0
    
    return pd.DataFrame(data)

def calculate_scores(pxp):
    """
    Calculate runs scored and delta run expectancy for each play
    
    pxp: DataFrame
        DataFrame of play by play data
        
    Returns:
        DataFrame of plays with runs_scored and delta_run_expectancy columns
    """
    pxp['runs_scored'] = pxp['bat_score'].shift(-1) - pxp['bat_score']
    mask = (pxp['inning_id'].eq(pxp['inning_id'].shift(-1))) & (pxp['game_id'].eq(pxp['game_id'].shift(-1)))
    pxp.loc[~mask, 'runs_scored'] = 0
    mask = pxp['inning_id'].eq(pxp['inning_id'].shift(-1))
    pxp.loc[mask, 'delta_run_expectancy'] = pxp.loc[mask, 'run_expectancy'].shift(
        -1) - pxp['run_expectancy'] + pxp.loc[mask, 'runs_scored']
    pxp.loc[~mask, 'delta_run_expectancy'] -= pxp.loc[~mask, 'run_expectancy']
    
    return pxp

def slope_intercept(df, x, y):
    '''
    

    Parameters
    ----------
    df : df
        A dataframe with a x column and y column.
    x : String
        Name of column in df that is independent variable.
    y : String
        Name of column in df that is target variable.

    Returns
    -------
    intercept : Int
    coefficient : INT

    '''
    X = df[[x]]
    y = df[y]
    model = LinearRegression().fit(X, y)
    intercept = model.intercept_
    coefficient = model.coef_[0]
    return intercept, coefficient

def linnear_func(df, x, y, intercept, coefficient):
    '''
    

    Parameters
    ----------
    df : df
        A dataframe with a x column and y column.
    x : String
        Name of column in df that is independent variable.
    y : String
        Name of column in df that is target variable.
    intercept : INT
    coefficient : INT

    Returns
    -------
    Series
        Returns a series of the y predicted from f(x).

    '''
    df[y] = df[x] * coefficient + intercept
    df[y] = df[y].clip(lower=0)
    return df[y]
