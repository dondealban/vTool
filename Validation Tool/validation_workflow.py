'''
Created on 03.09.2014

@author: rkope
'''

import numpy as np
import csv
from validation_functions import confusion_matrix, normalize, weight_based_on_area, divide, weightedMatrix, sumMatrix, diagonal, producers_users_accuracy, producersError, usersError 
from load_from_shape import vectorsFromShape

from kappa import kappa

class MadMex_Validation(object):
    
    def __init__(self,reference, predicted, labels, sqkm):
        self.reference = reference
        self.predicted = predicted
        self.labels = labels
        self.sqkm = sqkm
        self.producers_accuracy = None
        
    def validation_workflow(self):
        confmat = confusion_matrix(self.reference, self.predicted)
        cmn = normalize(confmat)
        cmn_normalized = divide(cmn, 100)
        weight = weight_based_on_area(self.sqkm)
        weighted_matrix = weightedMatrix(cmn_normalized, weight)
        [self.producers_accuracy, users_accuracy] = producers_users_accuracy(diagonal(weighted_matrix), sumMatrix(weighted_matrix,1), sumMatrix(weighted_matrix,0))
        [stratified_producers_error, p_error, producers_error, overall_producers_error] = producersError(confmat,weight,self.sqkm)
        [stratified_user_error, u_error, users_error, overall_users_error] = usersError(confmat,weight,self.sqkm)
        
        overall = np.nansum(diagonal(weighted_matrix))
        
        resultdict = dict()
        resultdict['labels'] = labels
        resultdict['Area'] = sqkm
        resultdict['Weights'] = weight
        resultdict['Weights in %'] = weight*100
        resultdict['Stratified Producers Error'] = stratified_producers_error
        resultdict['P Error(+-)'] = p_error
        resultdict['Producers Accuracy'] = self.producers_accuracy
        resultdict['Producers Error'] = producers_error
        resultdict['Overall Producers Error'] = overall_producers_error
        resultdict['Stratified User Error'] = stratified_user_error
        resultdict['U Error(+-)'] = u_error
        resultdict['Users Accuracy'] = users_accuracy
        resultdict['Users_error'] = users_error
        resultdict['Overall Users Error'] = overall_users_error
        resultdict['Overall Accuracy'] = overall
        resultdict['Weighted Matrix'] = weighted_matrix
        
        
        #print resultdict['Overall Accuracy']
        o = open("C:/test.csv", 'wb')
        result = csv.writer(o)
        test = "Test"
        result.writerow([overall_users_error])
        
        
if __name__=='__main__':
    
    #####    Jetzt derweil wird noch alles aus shapefile    #####
    input = "F:/valid/validation_2011_inside.shp"
    sqkm = np.array([421.0579,168802.1685,167063.9199,32317.5242,238239.9014,20848.5944,15468.8303,18846.1648,152143.6944,67534.4601,1656.3534,33161.1221,54016.6211,9126.5549,1305.4183,9912.4112,23135.6098,5663.3474,52880.8047,1537.8024,106691.7108,34020.1872,4723.3201,21575.9152,3801.0698,25496.8846,309880.4482,321902.6546,13733.5860,9985.8119,11208.5347,643.7893]) 
    [reference, predicted, labels] = vectorsFromShape(input,1,2)
    #####                                                   #####
    #input for validation: reference, predicted and labels column of shapefile and area in sqkm of each class
    #MV = MadMex_Validation(reference, predicted, labels, sqkm)
    #MV.validation_workflow()
    
    