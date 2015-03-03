'''
Created on 08.09.2014

@author: rkope
'''

import shp as shp
import numpy as np
from string import lower

def vectorsFromShape(input, refColNr, preColNr):
    shape = shp.Reader(input)
    recordsarray = np.array(shape.records())
    predicted = recordsarray[:,preColNr]
    for i in range(len(predicted)):
        predicted[i] = lower(str(int(float(predicted[i]))))     
    reference = recordsarray[:,refColNr]
    for i in range(len(reference)):
        reference[i] = lower(str(int(float(reference[i]))))
        reference[i] = lower(str(int(float(reference[i]))))
    
    predicted = predicted.astype(float)
    reference = reference.astype(float)
    labels = np.unique(np.concatenate((reference,predicted),1))
    labelsnumeric = np.arange(1,len(labels)+1)
    predictednumeric = predicted
    referencenumeric = reference
    for i in range(0,len(labels)):
        pidx = np.nonzero(predicted == labels[i])
        predictednumeric[pidx] = labelsnumeric[i]
        idx = np.nonzero(reference == labels[i])
        referencenumeric[idx] = labelsnumeric[i]         
    return reference, predicted, labels
    