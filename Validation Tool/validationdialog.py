# -*- coding: utf-8 -*-
"""
/***************************************************************************
 validationDialog
                                 A QGIS plugin
 Validation Tool for ESRI Shapefile based on scientific paper named "Making better use of accuracy data in land change studies: Estimating accuracy and area quantifying uncertainty using stratified estimation"
                             -------------------
        begin                : 2014-09-12
        copyright            : (C) 2014 by René Kopeinig
        email                : rene.kopeinig@conabio.gob.mx
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from collections import OrderedDict
import shp as shp
import csv
from string import lower
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from rk_validation import Ui_rkValidation
import numpy as np
from kappa import kappa
from validation_functions import accuracies, confusion_matrix, normalize, weight_based_on_area,\
     divide, weightedMatrix, sumMatrix, diagonal, producers_users_accuracy,\
     producersError, usersError
from help import *

class validationDialog(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_rkValidation()
        self.ui.setupUi(self)
        self.ui.pb_outFolder.clicked.connect(self.setOutput)
        self.ui.pb_uploadShape.clicked.connect(self.setInput)
        self.ui.pb_validate.clicked.connect(self.doValidation)
        self.ui.pb_close.clicked.connect(self.close)
        self.dialogTextBrowser = MyHelp(self)
        self.dialogTextBrowser.resize(500, 335)
        self.ui.pb_help.clicked.connect(self.on_pushButton_clicked)
        self.ui.cb_useWeight.hide()
        self.ui.pb_selectWeight.hide()
        self.ui.pb_selectWeight.clicked.connect(self.selectWeights)
        self.ui.pb_submitWeight.clicked.connect(self.sqkmInputToArray)
        #skqm based on inegi product for whole Mexico  #
        self.sqkm = np.array([421.0579,168802.1685,167063.9199,32317.5242,238239.9014,20848.5944,15468.8303,18846.1648,152143.6944,67534.4601,1656.3534,33161.1221,54016.6211,9126.5549,1305.4183,9912.4112,23135.6098,5663.3474,52880.8047,1537.8024,106691.7108,34020.1872,4723.3201,21575.9152,3801.0698,25496.8846,309880.4482,321902.6546,13733.5860,9985.8119,11208.5347,643.7893]) 
        #    #    #    #    #    #    #    #    #    #    #    #
        self.labels = None
        self.confmat = None
        self.weighted_matrix = None
        self.weight = None
        self.sqkm_vector = [] 
        self.cmn_normalized = None
        self.producers_accuracy = None
        self.user_accuracy = None
        self.stratified_producers_error = None
        self.p_error = None
        self.producers_error = None 
        self.overall_producers_error = None
        self.stratified_user_error = None
        self.u_error = None 
        self.users_error = None
        self.overall_users_error = None
        self.kappa = None
        self.outputFileName = None
        self.confnorm = None
        self.confnorm2 = None
   
    def sqkmInputToArray(self):
        self.ui.tabWidget.setCurrentIndex(0)
        try: 
            self.ui.tbl_setWeights.setRowCount(len(self.labels))
            numrows = self.ui.tbl_setWeights.rowCount()
            for row in range(numrows):
                item = float(self.ui.tbl_setWeights.item(row, 1).text())
                self.sqkm_vector.append(item)            
       
        except Exception, e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))

    def selectWeights(self):
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.cb_useWeight.setCheckState(True)
        [reference, predicted, self.labels] = self.vectorsFromFile(self.inputFileName, self.ui.le_refColNr.text(), self.ui.le_preColNr.text())
        
        self.ui.tbl_setWeights.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Labels"))
        self.ui.tbl_setWeights.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Weights"))
        
        tableHeader = self.ui.tbl_setWeights.horizontalHeader()
        tableHeader.setStretchLastSection(True)
        
        self.ui.tbl_setWeights.setRowCount(len(self.labels))
        for counter, i in enumerate(self.labels):
            self.ui.tbl_setWeights.setItem(counter, 0, QtGui.QTableWidgetItem(str(i)))
             
    def clean(self):
        self.ui.le_outFolder.clear()
        self.ui.le_inShapePath.clear()
        self.ui.le_refColNr.clear()
        self.ui.le_preColNr.clear()
        self.ui.cb_useWeight.setCheckState(False)
        self.inputFileName = None
        self.outputFileName = None      
    
    def doValidation(self):
        try:          
            if self.ui.cb_useWeight.isChecked() == True:
                referenceColNr = self.ui.le_refColNr.text()
                predictedColNr = self.ui.le_preColNr.text()
                [reference, predicted, self.labels] = self.vectorsFromFile(self.inputFileName, referenceColNr, predictedColNr)
                self.confmat = confusion_matrix(reference, predicted)
                [self.confnorm, self.confnorm2] = normalize(self.confmat)
                self.cmn_normalized = divide(self.confnorm, 100)
                self.weight = weight_based_on_area(self.sqkm_vector)
                
                QtGui.QMessageBox.about(self, "reference", str(len(reference)))
                QtGui.QMessageBox.about(self, "predicted", str(len(predicted)))
                QtGui.QMessageBox.about(self, "labels", str(len(self.labels)))
                """  
                weighted_cm = np.divide(self.confmat*1.0, np.nansum(self.confmat, axis=0))
                weighted_cm = np.nan_to_num(weighted_cm)
                
                QtGui.QMessageBox.about(self, "matrix sum", str(sum(weighted_cm)))
                QtGui.QMessageBox.about(self, "weight summe", str(self.weight))
                producers_area =  np.dot(weighted_cm, self.weight)
                QtGui.QMessageBox.about(self, "dot rotz", str(producers_area))"""
                
                #consider nur die klassen die tatsaechlich vorkommen im predicted.
                
                self.weighted_matrix = weightedMatrix(self.cmn_normalized, self.weight)
                [self.producers_accuracy, self.user_accuracy] = producers_users_accuracy(diagonal(self.weighted_matrix), sumMatrix(self.weighted_matrix,1), sumMatrix(self.weighted_matrix,0))
                [self.stratified_producers_error, self.p_error, self.producers_error, self.overall_producers_error] = producersError(self.confmat,self.weight,self.sqkm_vector)
                [self.stratified_user_error, self.u_error, self.users_error, self.overall_users_error] = usersError(self.confmat,self.weight,self.sqkm_vector)
                self.overall = np.nansum(diagonal(self.weighted_matrix))
                
            
            if self.ui.cb_useWeight.isChecked() == False:
                referenceColNr = self.ui.le_refColNr.text()
                predictedColNr = self.ui.le_preColNr.text()
                [reference, predicted, self.labels] = self.vectorsFromFile(self.inputFileName, referenceColNr, predictedColNr)
                self.confmat = confusion_matrix(reference, predicted)
                [self.confnorm, self.confnorm2] = normalize(self.confmat)
                self.cmn_normalized = divide(self.confnorm, 100)
                [self.overall_accuracy, self.producers_accuracy, self.user_accuracy] = accuracies(self.confnorm, self.confnorm2, self.confmat, np.sum(self.confmat,0))
                
            self.writeResult()
        except Exception, e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))
    
    def on_pushButton_clicked(self):
        self.dialogTextBrowser.exec_()
        
    def setInput(self):
        try:
            self.inputFileName = QtGui.QFileDialog.getOpenFileName(self,"Load ESRI Shapefile (.shp) or Shapefile attribute format (.dbf) ...","C:/", "SHP and DBF files (*.shp *.dbf)")
            self.ui.le_inShapePath.setText(self.inputFileName)
        except Exception,e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))
                
    def setOutput(self):
        try:
            self.outputFileName = QtGui.QFileDialog.getSaveFileName(self,"Save Validation...","C:/", "CSV file (*.csv)")
            self.ui.le_outFolder.setText(self.outputFileName)
        except Exception,e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))
            
    def vectorsFromFile(self, input, refColNr, preColNr):
        try: 
            input = str(input)
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
            self.labels = np.unique(np.concatenate((reference,predicted),1))
            labelsnumeric = np.arange(1,len(self.labels)+1)
            predictednumeric = predicted
            referencenumeric = reference
            for i in range(0,len(self.labels)):
                pidx = np.nonzero(predicted == self.labels[i])
                predictednumeric[pidx] = labelsnumeric[i]
                idx = np.nonzero(reference == self.labels[i])
                referencenumeric[idx] = labelsnumeric[i]         
            return reference, predicted, self.labels
        except Exception,e:
            QtGui.QMessageBox.about(self, "Error", "Writing CSV Error = %s" % str(e))
            
    def writeResult(self):
        try:
            if self.ui.cb_useWeight.isChecked() == True:
                if self.outputFileName == None:
                    o = open(self.inputFileName+"_weighted_based_validation.csv", "wb")
                if self.outputFileName != None:
                    o = open(self.outputFileName, "wb")  
                result = csv.writer(o)
                keys = ["Labels", "Weight","Weight in %","Stratified Producers Error",
                        "P-Error(+-)","Producers Accuracy", "Producer Error", 
                        "Stratified Users Error", "U-Error(+-)", "Users Accuracy", "Users Error"]
                value = zip(self.labels, self.weight, self.weight*100, self.stratified_producers_error, 
                           self.p_error, self.producers_accuracy, self.producers_error,
                           self.stratified_user_error, self.u_error, self.user_accuracy, self.users_error)
                result.writerow([" "])
                result.writerow(keys)
                for i in value:
                    result.writerow(i)
                result.writerow([" "])
                result.writerow(["Sum Results", np.nansum(self.weight),np.nansum(self.weight*100), np.nansum(self.stratified_producers_error),np.nansum(self.p_error),
                                 np.nansum(self.producers_accuracy), np.nansum(self.producers_error), np.nansum(self.stratified_user_error), 
                                 np.nansum(self.u_error), np.nansum(self.user_accuracy), np.nansum(self.users_error)])
                result.writerow([" "])
                result.writerow(["Overall Producers Error","Overall Users Error", "Overall Accuracy"])
                result.writerow([self.overall_producers_error, self.overall_users_error, self.overall])
                result.writerow([" "])
                result.writerow(["Weighted Matrix"])
                result.writerows(self.weighted_matrix)
                o.close() 
                if self.outputFileName == None:
                    QtGui.QMessageBox.about(self, "Information", "Validation successfully executed. <br> File saved as "+str(self.inputFileName+"_weighted_based_validation.csv"))
                else:
                    QtGui.QMessageBox.about(self, "Information", "Validation successfully executed. <br> File saved as "+str(self.outputFileName))   
                    
            if self.ui.cb_useWeight.isChecked() == False:
                if self.outputFileName == None:
                    o = open(self.inputFileName+"_validation.csv", "wb")
                else:
                    o = open(self.outputFileName, "wb")   
                result = csv.writer(o)
                keys = ["Labels", "Producers Accuracy", "Users Accuracy"]
                value = zip(self.labels, self.producers_accuracy, self.user_accuracy)
                result.writerow(["Overall Accuracy"])
                result.writerow([self.overall_accuracy])
                result.writerow([" "])
                result.writerow(keys)
                for i in value:
                    result.writerow(i)
                result.writerow([" "])
                result.writerow(["Confusion Matrix"])
                result.writerows(self.confnorm)
                result.writerow([" "])
                result.writerow([" "])
                result.writerow(["Normalized Confusion Matrix"])
                result.writerows(self.cmn_normalized)                
                
                o.close()
                if self.outputFileName == None:
                    QtGui.QMessageBox.about(self, "Information", "Validation successfully executed. <br> File saved as "+str(self.inputFileName+"_validation.csv"))
                else:
                    QtGui.QMessageBox.about(self, "Information", "Validation successfully executed. <br> File saved as "+str(self.outputFileName))    
            self.clean()
        except Exception, e:
            QtGui.QMessageBox.about(self, "Error", "Writing CSV Error = %s" % str(e))
            
class MyHelp(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MyHelp, self).__init__(parent)
        self.setWindowTitle("Help")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.clicked.connect(self.close)
        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.append(input_h)
        self.textBrowser.append(input)
        self.textBrowser.append(output_h)
        self.textBrowser.append(output)
        self.textBrowser.append(validation_h)
        self.textBrowser.append(validation)
        self.textBrowser.append(info_h)
        self.textBrowser.append(info)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)