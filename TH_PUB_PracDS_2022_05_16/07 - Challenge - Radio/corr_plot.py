'''plots a heatmap of correlation between a set of statistics vs
another set

'''

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def corr_coeff(col1, col2):
    return np.corrcoef(col1, col2)[0,1]

def corr_matrix(data1, features1, data2, features2):
    result = np.zeros((len(features2), len(features1)))
    for jj, f2 in enumerate(features2):
        for ii, f1 in enumerate(features1):
            col1 = data1[f1]
            col2 = data2[f2]
            result[jj, ii] = corr_coeff(col1, col2)
    return result

def plot_corr_heatmap(data1, features1, data2, features2,
                      scale=1.0, **opts):
    corr_mat = corr_matrix(data1, features1, data2, features2)
    if 'ax' not in opts:
        fig, ax = plt.subplots(figsize=(0.5*len(features1)*scale,
                                        0.5*len(features2)*scale))
        opts['ax'] = ax
    if 'cmap' not in opts:
        opts['cmap'] = sns.diverging_palette(220, 10, as_cmap=True)
    if 'cbar_kws' not in opts:
        # rotate the colorbar to horizontal if x dim is greater than y dim
        if len(features1) > len(features2):
            location = 'top'
        else:
            location = 'right'
            opts['cbar_kws'] = {'use_gridspec': False,
                                'location': location,
                                'shrink': 0.5}
    if 'square' not in opts:
        opts['square'] = True
        _ = sns.heatmap(corr_mat,
                        vmax = corr_mat.max(),
                        vmin = corr_mat.min(),
                        center = 0.0, linewidth=.5,
                        xticklabels = features1,
                        yticklabels = features2,
                        **opts)
    return _

def plot_corr_ranking(data1, main_feature, data2, features2,
                      scale=(1.0, 1.0), xlim=(-1,1), **opts):
    corr_mat = corr_matrix(data1, [main_feature], data2, features2)
    if 'ax' not in opts:
        fig, ax = plt.subplots(figsize=(5 * scale[0],
                                        len(features2) * 0.5 * scale[1]))
        ax.set_xlim(xlim)
        opts['ax'] = ax

    corr_data = pd.DataFrame({'features': features2,
                              'corr coeff': corr_mat[:, 0]})
    corr_data = corr_data.sort_values('corr coeff', ascending=False)
    _ = sns.barplot(x = corr_data['corr coeff'],
                    y = corr_data['features'],
                    **opts)
    return _
