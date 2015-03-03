'''
Created on 15.09.2014

@author: rkope
'''

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.font_manager as font_manager
from pylab import *
import numpy as np
import itertools

def accuracies(confnorm, confnorm2, confmat, sx):
    producersaccuracy = np.diag(confnorm)
    usersaccuracy = np.diag(confnorm2)
    overallaccuracy = 100*float(sum(np.diag(confmat)))/sum((sx))
    return (overallaccuracy,producersaccuracy,usersaccuracy)


def confusion_matrix(reference, predicted):
    """
    Calculates confusion matrix out of reference and predicted list
    
    :param reference: List of reference values
    :type reference: list
    
    :param predicted: List of predicted values
    :type predicted: list
    """
    classes = list(set(reference))
    n = len(classes)
    cm = np.array([z.count(x) for z in [zip(reference,predicted)] for x in itertools.product(classes,repeat=2)]).reshape(n,n)
    return cm

def diagonal(matrix):
    return np.diagonal(matrix)

def divide(value1,value2):
    return np.divide(value1,value2)

def kappa(y_true, y_pred, weights=None, allow_off_by_one=False):
    """
    Calculates Kappa coefficient with help of lists reference and predicted 
    classification output values
    
    :param y_true: List of reference values
    :type y_true: list
    
    :param y_pred: List of predicted values
    :type y_pred: list
    
    :param weights: Value of weight (optional)
    :type weights: value
    
    :param allow_off_by_one: Value of allow_off_by_one (optional)
    :type allow_off_by_one: value
    """
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
    if np.count_nonzero(weights):
        k -= (sum(sum(weights * observed)) / sum(sum(weights * expected)))
    return k

def multiply(value1,value2):
    return np.multiply(value1,value2)

def n_1(i):
    t = np.tile(1,(len(i)))
    return i-t

def normalize(confmat):
    """
    Normalizes confusion matrix
    
    :param confmat: Confusion matrix
    :type confmat: array
    
    :param confnorm: Normalized confusion matrix
    :type confnorm: array
    """
    confnorm = np.zeros(confmat.shape)
    confnorm2 = np.zeros(confmat.shape)
    sy = sum(confmat,0)
    sx = sum(confmat,1)
    for i in range(0,sx.shape[0]):
            if sx[i] > 0:
                confnorm[i,:] = (confmat[i,:]).astype(float)/sx[i]*100  
    for i in range(0,sy.shape[0]):
        if sy[i] > 0:
            confnorm2[i,:] = (confmat[i,:]).astype(float)/sy[i]*100        
    return confnorm, confnorm2

def producers_users_accuracy(wdiag, sum_colum_wise, sum_row_wise):
    """
    Calculates producers and users accuracy
    
    :param wdiag: Diagonal of weighted matrix
    :type wdiag: list
    
    :param sum_colum_wise: Column-wised sum of weighted matrix
    :type sum_colum_wise: list
    
    :param sum_row_wise: Row-wised sum of weighted matrix
    :type sum_row_wise: list
    """
    producers_accuracy = wdiag/sum_colum_wise
    users_accuracy = wdiag/sum_row_wise
    return producers_accuracy, users_accuracy

def usersError(cm, weight, sqkm):
    """
    Calculates users error
    
    :param cm: Confusion matrix
    :type cm: array
    
    :param weight: List of weights based on area
    :type weight: list
    
    :param sqkm: List of square kilometre based on Inegi areas persistentes of each class
    :type sqkm: list
    """
    cm_transposed = transpose(cm)
    sum_row_cm_transposed = sumMatrix(cm_transposed, 0)
    
    sum_row_cm_transposed_1 = n_1(sum_row_cm_transposed)
    weighted_cm = divide(cm_transposed*1.0,np.nansum(cm_transposed,axis=0))
    
    users_area = multiply(weighted_cm, weight)
    users_standard_error = standardError(weight, weighted_cm, sum_row_cm_transposed_1)
    
    users_area_sum = sumMatrix(users_area,1)
    users_standard_error_sum = sumMatrix(users_standard_error,1)
        
    s_pj = sqrt(users_standard_error_sum)
    s_aj = multiply(s_pj, np.nansum(sqkm))
    s_aj_sum = np.nansum(s_aj)
    s_aj_2 = s_aj+s_aj
    s_aj_sum_2 = s_aj_sum+s_aj_sum
    
    aj = multiply(users_area_sum, np.nansum(sqkm))
    aj_sum = np.nansum(aj)
    users_error = divide(s_aj_2, aj)
    overall_users_error = divide(s_aj_sum_2, aj_sum)
    return aj, s_aj_2, users_error, overall_users_error

def producersError(cm,weight,sqkm):
    """
    Calculates producers error
    
    :param cm: Confusion matrix
    :type cm: array
    
    :param weight: List of weights based on area
    :type weight: list
    
    :param sqkm: List of square kilometre based on Inegi areas persistentes of each class
    :type sqkm: list
    """
    sum_row_cm = sumMatrix(cm,0)
    
    sum_row_cm_1  = n_1(sum_row_cm)
    weighted_cm = divide(cm*1.0,np.nansum(cm,axis=0)) #calcWeightedAbsolutMatrix
    producers_area =  multiply(weighted_cm, weight)
    producers_standard_error = standardError(weight, weighted_cm, sum_row_cm_1)     
    producers_area_sum = sumMatrix(producers_area,1)
    producers_standard_error_sum = sumMatrix(producers_standard_error,1)
    
    s_pj = sqrt(producers_standard_error_sum)
    s_aj = multiply(s_pj, np.nansum(sqkm))
    s_aj_sum = np.nansum(s_aj)
    s_aj_2 = s_aj+s_aj
    s_aj_sum_2 = s_aj_sum+s_aj_sum
    
    aj = multiply(producers_area_sum, np.nansum(sqkm))
    aj_sum = np.nansum(aj)
    producers_error = divide(s_aj_2, aj)
    overall_producers_error = divide(s_aj_sum_2, aj_sum)
    return aj, s_aj_2, producers_error, overall_producers_error

def standardError(weight, matrix, sum_row_matrix_1):
    """
    Calculates standard error
    
    :param weight: List of weights based on area
    :type weight: list
    
    :param matrix: Input matrix
    :type matrix: array
    
    :param sum_row_matrix_1: Row-wised matrix sum
    :type sum_row_matrix_1: list
    """
    sqweight = square(weight)
    return (sqweight*matrix*(matrix-1)/sum_row_matrix_1)*-1

def sqrt(value):
    return np.sqrt(value)

def square(value):
    return np.square(value)

def sumMatrix(matrix,axis):
    return np.nansum(matrix,axis=axis)

def transposeMatrix(matrix):
    return np.transpose(matrix)

def weight_based_on_area(area):
    return divide(area, np.nansum(area))

def weightedMatrix(matrix, weight):
    """
    Calculates weighted matrix
    
    :param matrix: Input matrix
    :type matrix: array
    
    :param weight: List of weights based on area
    :type weight: list
    """
    weighted_matrix = []
    for i in range(len(matrix)):
        result = matrix[i]*weight[i]
        weighted_matrix.append(result)
    return weighted_matrix
