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
from subprocess import Popen
import shp as shp
import csv
from osgeo import ogr
from string import lower
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from rk_validation import Ui_rkValidation
import numpy as np
from validation_functions import accuracies, confusion_matrix, normalize, objectCount, weight_based_on_area,\
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
        self.ui.tbl_setWeights.setSortingEnabled(False)
        self.ui.pb_selectWeight.clicked.connect(self.setAreaManually)
        self.ui.pb_selectWeight_csv.clicked.connect(self.setAreaCsv)
        self.ui.pb_submitWeight.clicked.connect(self.setAreaInputToArray)
        self.ui.rb_noweight.setChecked(True)
        self.ui.rb_noweight.clicked.connect(self.hide_gb_weights)
        self.ui.rb_weight.clicked.connect(self.show_gb_weights)
        self.hide_gb_weights()
        self.cmn_normalized = None
        self.confmat = None
        self.confnorm = None
        self.confnorm2 = None
        self.count_obj = None
        self.headerList = []
        self.labels = None
        self.outputFileName = None
        self.overall_producers_error = None
        self.overall_users_error = None
        self.p_error = None
        self.predicted = None
        self.producers_accuracy = None
        self.producers_error = None 
        self.reference = None
        self.sqkm_vector = [] 
        self.stratified_producers_error = None
        self.stratified_user_error = None
        self.u_error = None 
        self.user_accuracy = None
        self.users_error = None        
        self.weight = None
        self.weighted_matrix = None
        
    def calculateVectors(self):
        [referenceColNr, predictedColNr] = self.getColNr()
        [self.reference, self.predicted, self.labels] = self.vectorsFromFile(self.inputFileName, referenceColNr, predictedColNr)
        
    def clean(self):
        self.cleanCb()
        self.cleanTblWdgt()
        self.ui.le_outFolder.clear()
        self.ui.le_inShapePath.clear()
        self.ui.le_weightFromCSV.clear()
        self.ui.cb_useWeight.setCheckState(False)
        self.inputFileName = None
        self.outputFileName = None    
    
    def cleanCb(self):
        self.ui.cb_refCol.clear()
        self.ui.cb_preCol.clear()
    
    def cleanTblWdgt(self):
        self.ui.tbl_setWeights.clear()
        self.sqkm_vector = []
                
    def doValidation(self):
        try:
            self.calculateVectors()    
            self.confmat = confusion_matrix(self.reference, self.predicted)
            self.count_obj = objectCount(self.confmat)
            [self.confnorm, self.confnorm2] = normalize(self.confmat)
            self.cmn_normalized = divide(self.confnorm, 100)
                
            if self.ui.cb_useWeight.isChecked() == True:
                self.weight = weight_based_on_area(self.sqkm_vector)
                self.weighted_matrix = weightedMatrix(self.cmn_normalized, self.weight)
                [self.producers_accuracy, self.user_accuracy] = producers_users_accuracy(diagonal(self.weighted_matrix), sumMatrix(self.weighted_matrix,1), sumMatrix(self.weighted_matrix,0))
                [self.stratified_producers_error, self.p_error, self.producers_error, self.overall_producers_error] = producersError(self.confmat,self.weight,self.sqkm_vector)
                [self.stratified_user_error, self.u_error, self.users_error, self.overall_users_error] = usersError(self.confmat,self.weight,self.sqkm_vector)
                self.overall = np.nansum(diagonal(self.weighted_matrix))
                
            if self.ui.cb_useWeight.isChecked() == False:
                [self.overall_accuracy, self.producers_accuracy, self.user_accuracy] = accuracies(self.confnorm, self.confnorm2, self.confmat, np.sum(self.confmat,0))
            
            self.writeResult()
        
        except Exception, e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))
    
    def getColumnHeader(self):
        self.getHeaderNames()
        self.ui.cb_refCol.addItems(self.headerList)
        self.ui.cb_preCol.addItems(self.headerList)
        self.ui.cb_refCol.setCurrentIndex(0)
        self.ui.cb_preCol.setCurrentIndex(1)
        
    def getHeaderNames(self):
        self.headerList = []
        dataSource = ogr.Open(self.inputFileName)
        lyr = dataSource.GetLayer(0)
        layerDefinition = lyr.GetLayerDefn()
        
        for i in range(layerDefinition.GetFieldCount()):
            self.headerList.append(layerDefinition.GetFieldDefn(i).GetName())
    
    def getColNr(self):
        ref = self.headerList.index(self.ui.cb_refCol.currentText())
        pre = self.headerList.index(self.ui.cb_preCol.currentText())
        return ref, pre
    
    def hide_gb_weights(self):
        self.ui.pb_selectWeight_csv.setEnabled(False)
        self.ui.pb_selectWeight.setEnabled(False)
        self.ui.le_weightFromCSV.setEnabled(False)
            
    def show_gb_weights(self):
        self.ui.pb_selectWeight_csv.setEnabled(True)
        self.ui.pb_selectWeight.setEnabled(True)
        self.ui.le_weightFromCSV.setEnabled(True)
        
    def on_pushButton_clicked(self):
        self.dialogTextBrowser.exec_()
        
    def setInput(self):
        try:
            self.inputFileName = QtGui.QFileDialog.getOpenFileName(self,"Load ESRI Shapefile (.shp) or Shapefile attribute format (.dbf) ...","C:/", "SHP and DBF files (*.shp *.dbf)")
            self.ui.le_inShapePath.setText(self.inputFileName)
            self.cleanCb()
            self.getColumnHeader()
        except Exception,e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))
                
    def setInputCsv(self):
        try:
            input_csv = QtGui.QFileDialog.getOpenFileName(self, "Load CSV file (.csv) with single vector and without header ...", "C:/", "Only CSV files (*.csv)")
            self.ui.le_weightFromCSV.setText(input_csv)
            area = []
            try:
                reader = csv.reader(open(input_csv, "rU"))
                for row in reader:
                    area.append(float(row[0]))
                return area
            except Exception, e:
                QtGui.QMessageBox.about(self, "Error", "CSV Error = %s" %str(e))
        except Exception, e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" %str(e))
            
    def setOutput(self):
        try:
            self.outputFileName = QtGui.QFileDialog.getSaveFileName(self,"Save Validation...","C:/", "CSV file (*.csv)")
            self.ui.le_outFolder.setText(self.outputFileName)
        except Exception,e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))
            
    def setAreaInputToArray(self):
        self.ui.tabWidget.setCurrentIndex(0)
        try: 
            self.ui.tbl_setWeights.setRowCount(len(self.labels))
            numrows = self.ui.tbl_setWeights.rowCount()
            for row in range(numrows):
                item = float(self.ui.tbl_setWeights.item(row, 1).text())
                self.sqkm_vector.append(item)            
       
        except Exception, e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))

    def setAreaManually(self):
        try:
            self.cleanTblWdgt()
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.cb_useWeight.setCheckState(True)
            self.calculateVectors()
            self.ui.tbl_setWeights.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Labels"))
            self.ui.tbl_setWeights.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Weights"))
            
            tableHeader = self.ui.tbl_setWeights.horizontalHeader()
            tableHeader.setStretchLastSection(True)
            
            self.ui.tbl_setWeights.setRowCount(len(self.labels))
            for counter, i in enumerate(self.labels):
                self.ui.tbl_setWeights.setItem(counter, 0, QtGui.QTableWidgetItem(str(i)))
        except Exception, e:
            QtGui.QMessageBox.about(self, "Error", "Application Error = %s" % str(e))
            
    def setAreaCsv(self):
        try:
            self.cleanTblWdgt()
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.cb_useWeight.setCheckState(True)
            self.calculateVectors()
            self.ui.tbl_setWeights.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Labels"))
            self.ui.tbl_setWeights.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Weights"))
            
            tableHeader = self.ui.tbl_setWeights.horizontalHeader()
            tableHeader.setStretchLastSection(True)
            
            area = self.setInputCsv()
            self.ui.tbl_setWeights.setRowCount(len(self.labels))
            for counter, i in enumerate(self.labels):
                self.ui.tbl_setWeights.setItem(counter, 0, QtGui.QTableWidgetItem(str(i)))
            
            self.ui.tbl_setWeights.setRowCount(len(area))
            for counter, i in enumerate(area):
                self.ui.tbl_setWeights.setItem(counter, 1, QtGui.QTableWidgetItem(str(i)))
        except Exception, e:
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
            labels = np.unique(np.concatenate((reference,predicted),1))
            labels = np.array(labels)
            labelsnumeric = np.arange(1,len(labels)+1)
            predictednumeric = predicted
            referencenumeric = reference
            for i in range(0,len(labels)):
                pidx = np.nonzero(predicted == labels[i])
                predictednumeric[pidx] = labelsnumeric[i]
                idx = np.nonzero(reference == labels[i])
                referencenumeric[idx] = labelsnumeric[i]         
            return reference, predicted, labels
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
                keys = ["Labels", "Occurrences", "Area", "Weight","Weight in %","Stratified Producers Area Estimation",
                    "Producers Area Standard Error","Producers Accuracy", "Producer Standard Error", 
                    "Stratified Users Area Estimation", "Users Area Standard Error", "Users Accuracy", "Users Standard Error"]
                value = zip(self.labels, self.count_obj, self.sqkm_vector, self.weight, self.weight*100, self.stratified_producers_error, 
                           self.p_error, self.producers_accuracy, self.producers_error,
                           self.stratified_user_error, self.u_error, self.user_accuracy, self.users_error)
                result.writerow([" "])
                result.writerow(keys)
                for i in value:
                    result.writerow(i)
                result.writerow([" "])
                result.writerow(["Sum Results", np.nansum(self.count_obj), np.nansum(self.sqkm_vector), np.nansum(self.weight),np.nansum(self.weight*100), np.nansum(self.stratified_producers_error),np.nansum(self.p_error),
                                 np.nansum(self.producers_accuracy), np.nansum(self.producers_error), np.nansum(self.stratified_user_error), 
                                 np.nansum(self.u_error), np.nansum(self.user_accuracy), np.nansum(self.users_error)])
                result.writerow([" "])
                result.writerow(["Overall Producers Error","Overall Users Error", "Overall Accuracy"])
                result.writerow([self.overall_producers_error, self.overall_users_error, self.overall])
                result.writerow([" "])
                result.writerow(["Absolute Matrix"])
                confmat = np.insert(self.confmat,0, self.labels, axis=1)
                confmat = np.insert(confmat, 0, np.insert(self.labels,0,0), axis=0)
                result.writerows(confmat)
                result.writerow([" "])
                result.writerow(["Weighted Matrix"])
                weighted_matrix = np.insert(self.weighted_matrix,0, self.labels, axis=1)
                weighted_matrix = np.insert(weighted_matrix, 0, np.insert(self.labels,0,0), axis=0)
                result.writerows(weighted_matrix)
                o.close() 
                if self.outputFileName == None:
                    self.outputFileName = self.inputFileName+"_weight_based_validation.csv"
                    QtGui.QMessageBox.about(self, "Information", "Validation successfully executed. <br> File saved as "+str(self.outputFileName))
                    
                else:
                    QtGui.QMessageBox.about(self, "Information", "Validation successfully executed. <br> File saved as "+str(self.outputFileName))
                    
                   
            if self.ui.cb_useWeight.isChecked() == False:
                if self.outputFileName == None:
                    o = open(self.inputFileName+"_validation.csv", "wb")
                else:
                    o = open(self.outputFileName, "wb")   
                result = csv.writer(o)
                keys = ["Labels", "Occurrences", "Producers Accuracy", "Users Accuracy"]
                value = zip(self.labels, self.count_obj, self.producers_accuracy, self.user_accuracy)
                result.writerow(["Overall Accuracy"])
                result.writerow([self.overall_accuracy])
                result.writerow([" "])
                result.writerow(keys)
                for i in value:
                    result.writerow(i)
                result.writerow([" "])
                result.writerow(["Sum Results", np.nansum(self.count_obj), np.nansum(self.producers_accuracy), np.nansum(self.user_accuracy)])
                result.writerow([" "])
                result.writerow(["Absolute Matrix"])
                confmat = np.insert(self.confmat,0, self.labels, axis=1)
                confmat = np.insert(confmat, 0, np.insert(self.labels,0,0), axis=0)
                result.writerows(confmat)
                result.writerow([" "])
                result.writerow(["Confusion Matrix 1"])
                confnorm = np.insert(self.confnorm,0, self.labels, axis=1)
                confnorm = np.insert(confnorm, 0, np.insert(self.labels,0,0), axis=0)
                result.writerows(confnorm)
                result.writerow([" "])
                result.writerow(["Confusion Matrix 2"])
                confnorm2 = np.insert(self.confnorm2,0, self.labels, axis=1)
                confnorm2 = np.insert(confnorm2, 0, np.insert(self.labels,0,0), axis=0)
                result.writerows(confnorm2)
                result.writerow([" "])
                result.writerow(["Normalized Confusion Matrix"])
                cmn_normalized = np.insert(self.cmn_normalized,0, self.labels, axis=1)
                cmn_normalized = np.insert(cmn_normalized, 0, np.insert(self.labels,0,0), axis=0)
                result.writerows(cmn_normalized)                
                
                o.close()
                if self.outputFileName == None:
                    self.outputFileName = self.inputFileName+"_validation.csv"
                    QtGui.QMessageBox.about(self, "Information", "Validation successfully executed. <br> File saved as "+str(self.outputFileName))
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
        self.textBrowser.append(input_csv_h)
        self.textBrowser.append(input_csv)
        self.textBrowser.append(output_h)
        self.textBrowser.append(output)
        self.textBrowser.append(validation_h)
        self.textBrowser.append(validation)
        self.textBrowser.append(info_h)
        self.textBrowser.append(info)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)