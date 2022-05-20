'''Collection of useful functions for performing statistical tests
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import math

def significance(p_value):
    '''get significance based on test p value

    '''
    if p_value < 0.001:
        return 'extremely'
    elif p_value < 0.01:
        return 'highly'
    elif p_value < 0.05:
        return 'significant'
    else:
        return 'not significant'

def ttest_features(data, features):
    '''does the null hypothesis test between two data frames for a given
    set of features. Both data frames must contain all the columns in
    the list of features.

    input:

    data: must be a dictionary {name1: dataframe1, name2: dataframe2}
          where name1 and name2 are strings --- name given to the data sets
    features:  must be a list of strings denoting the columns to be tested

    '''
    names = []
    dfs = []
    for name, df in data.items():
        names.append(name)
        dfs.append(df)

    ttest_p = []
    difference = []
    for feature in features:
        t, p = stats.ttest_ind(dfs[0][feature],
                               dfs[1][feature])
        ttest_p.append(p)
        difference.append(significance(p))

    n1 = 'N '+names[0]
    n2 = 'N '+names[1]
    result = pd.DataFrame(
        {'features': features,
         n1: len(dfs[0]),
         n2: len(dfs[1]),
         'ttest p': ttest_p,
         'significance': difference
        }
    )
    return result[['features',
                   n1,
                   n2,
                   'ttest p',
                   'significance'
                  ]].sort_values('ttest p')


def plot_dist_compare(data, features, figsize=None, **opts):
    '''plots one distribution for each of the features for all of the
    dataframes included in data.

    input:

    data: must be a dictionary {name1: dataframe1, name2: dataframe2, ...}
          where name1 and name2 are strings --- name given to the data sets
    features:  must be a list of strings denoting the columns to be tested

    '''
    # calculate figure size and number of subplots needed
    dim = len(features)
    cols = 2 if dim >= 2 else 1
    rows = math.ceil(dim / cols)

    if figsize is None:
        figsize = (cols * 5, rows * 5)

    fig, ax = plt.subplots(rows, cols, figsize=figsize)

    # create dataframe for plot
    dfs = []
    for name, df in data.items():
        df1 = df.copy()
        df1['sample'] = name
        dfs.append(df1)
    df = pd.concat(dfs)
    df['count'] = ''

    # do split plot if we are comparing two things
    split = True if len(dfs) == 2 else False

    for ind, feature in enumerate(features):
        if dim == 1:
            axis = ax
        elif dim == 2:
            axis = ax[ind]
        else:
            axis = ax[ind//2, ind%2]
        sns.violinplot(data = df,
                       x = feature,
                       y = 'count',
                       hue = 'sample',
                       split = split,
                       inner = 'quartile',
                       ax = axis,
                       **opts)

    return fig
