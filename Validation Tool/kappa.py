'''
Created on 05.09.2014

@author: rkope
'''

import numpy as np
from six import string_types
from validation_functions import confusion_matrix

def kappa(y_true, y_pred, weights=None, allow_off_by_one=False):
    y_true = [int(np.round(float(y))) for y in y_true]
    y_pred = [int(np.round(float(y))) for y in y_pred]
    
    min_rating = min(min(y_true), min(y_pred))
    max_rating = max(max(y_true), max(y_pred))

    y_true = [y - min_rating for y in y_true]
    y_pred = [y - min_rating for y in y_pred]

    num_ratings = max_rating - min_rating + 1
    observed = confusion_matrix(y_true, y_pred)
    num_scored_items = float(len(y_true))
    

    if isinstance(weights, string_types):
        wt_scheme = weights
        weights = None
    else:
        wt_scheme = ''
    if weights is None:
        weights = np.empty((num_ratings, num_ratings))
        for i in range(num_ratings):
            for j in range(num_ratings):
                diff = abs(i - j)
                if allow_off_by_one and diff:
                    diff -= 1
                if wt_scheme == 'linear':
                    weights[i, j] = diff
                elif wt_scheme == 'quadratic':
                    weights[i, j] = diff ** 2
                elif not wt_scheme:
                    weights[i, j] = bool(diff)
                else:
                    raise ValueError(('Incorrect weight schema for ' +
                                      'kappa: {}').format(wt_scheme))
    
    hist_true = np.bincount(y_true, minlength=num_ratings)
    hist_true = hist_true[: num_ratings] / num_scored_items
    hist_pred = np.bincount(y_pred, minlength=num_ratings)
    hist_pred = hist_pred[: num_ratings] / num_scored_items
    expected = np.outer(hist_true, hist_pred)
    
    observed = observed / num_scored_items
    
    k = 1.0
    print len(weights), len(observed), len(expected)
    if np.count_nonzero(weights):
        k -= (sum(sum(weights * observed)) / sum(sum(weights * expected)))
    return k