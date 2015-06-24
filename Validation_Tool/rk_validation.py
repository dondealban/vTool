# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rk_validation.ui'
#
# Created: Mon Oct 27 17:48:37 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_rkValidation(object):
    def setupUi(self, rkValidation):
        rkValidation.setObjectName(_fromUtf8("rkValidation"))
        rkValidation.resize(549, 495)
        self.pb_close = QtGui.QPushButton(rkValidation)
        self.pb_close.setGeometry(QtCore.QRect(455, 460, 75, 23))
        self.pb_close.setObjectName(_fromUtf8("pb_close"))
        self.pb_help = QtGui.QPushButton(rkValidation)
        self.pb_help.setGeometry(QtCore.QRect(370, 460, 75, 23))
        self.pb_help.setObjectName(_fromUtf8("pb_help"))
        self.tabWidget = QtGui.QTabWidget(rkValidation)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 521, 441))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tb_main = QtGui.QWidget()
        self.tb_main.setObjectName(_fromUtf8("tb_main"))
        self.gb3 = QtGui.QGroupBox(self.tb_main)
        self.gb3.setGeometry(QtCore.QRect(10, 330, 171, 71))
        self.gb3.setObjectName(_fromUtf8("gb3"))
        self.pb_validate = QtGui.QPushButton(self.gb3)
        self.pb_validate.setGeometry(QtCore.QRect(10, 25, 151, 31))
        self.pb_validate.setObjectName(_fromUtf8("pb_validate"))
        self.gb2 = QtGui.QGroupBox(self.tb_main)
        self.gb2.setGeometry(QtCore.QRect(10, 250, 491, 71))
        self.gb2.setObjectName(_fromUtf8("gb2"))
        self.le_outFolder = QtGui.QLineEdit(self.gb2)
        self.le_outFolder.setGeometry(QtCore.QRect(210, 30, 261, 20))
        self.le_outFolder.setObjectName(_fromUtf8("le_outFolder"))
        self.pb_outFolder = QtGui.QPushButton(self.gb2)
        self.pb_outFolder.setGeometry(QtCore.QRect(10, 30, 151, 21))
        self.pb_outFolder.setObjectName(_fromUtf8("pb_outFolder"))
        self.cb_useWeight = QtGui.QCheckBox(self.tb_main)
        self.cb_useWeight.setGeometry(QtCore.QRect(320, 360, 101, 21))
        self.cb_useWeight.setObjectName(_fromUtf8("cb_useWeight"))
        self.gb1 = QtGui.QGroupBox(self.tb_main)
        self.gb1.setGeometry(QtCore.QRect(10, 10, 491, 121))
        self.gb1.setObjectName(_fromUtf8("gb1"))
        self.pb_uploadShape = QtGui.QPushButton(self.gb1)
        self.pb_uploadShape.setGeometry(QtCore.QRect(10, 19, 151, 21))
        self.pb_uploadShape.setObjectName(_fromUtf8("pb_uploadShape"))
        self.le_inShapePath = QtGui.QLineEdit(self.gb1)
        self.le_inShapePath.setGeometry(QtCore.QRect(210, 20, 261, 21))
        self.le_inShapePath.setObjectName(_fromUtf8("le_inShapePath"))
        self.lb_preColNr = QtGui.QLabel(self.gb1)
        self.lb_preColNr.setGeometry(QtCore.QRect(210, 50, 51, 20))
        self.lb_preColNr.setObjectName(_fromUtf8("lb_preColNr"))
        self.lb_refColNr = QtGui.QLabel(self.gb1)
        self.lb_refColNr.setGeometry(QtCore.QRect(10, 50, 51, 20))
        self.lb_refColNr.setObjectName(_fromUtf8("lb_refColNr"))
        self.cb_preCol = QtGui.QComboBox(self.gb1)
        self.cb_preCol.setGeometry(QtCore.QRect(210, 70, 151, 22))
        self.cb_preCol.setObjectName(_fromUtf8("cb_preCol"))
        self.cb_refCol = QtGui.QComboBox(self.gb1)
        self.cb_refCol.setGeometry(QtCore.QRect(10, 70, 151, 22))
        self.cb_refCol.setObjectName(_fromUtf8("cb_refCol"))
        self.rb_weight = QtGui.QRadioButton(self.gb1)
        self.rb_weight.setGeometry(QtCore.QRect(380, 60, 91, 17))
        self.rb_weight.setObjectName(_fromUtf8("rb_weight"))
        self.rb_noweight = QtGui.QRadioButton(self.gb1)
        self.rb_noweight.setGeometry(QtCore.QRect(380, 80, 82, 17))
        self.rb_noweight.setObjectName(_fromUtf8("rb_noweight"))
        self.gb4 = QtGui.QGroupBox(self.tb_main)
        self.gb4.setGeometry(QtCore.QRect(10, 140, 491, 101))
        self.gb4.setObjectName(_fromUtf8("gb4"))
        self.pb_selectWeight = QtGui.QPushButton(self.gb4)
        self.pb_selectWeight.setGeometry(QtCore.QRect(10, 60, 151, 21))
        self.pb_selectWeight.setObjectName(_fromUtf8("pb_selectWeight"))
        self.pb_selectWeight_csv = QtGui.QPushButton(self.gb4)
        self.pb_selectWeight_csv.setGeometry(QtCore.QRect(10, 25, 151, 21))
        self.pb_selectWeight_csv.setObjectName(_fromUtf8("pb_selectWeight_csv"))
        self.le_weightFromCSV = QtGui.QLineEdit(self.gb4)
        self.le_weightFromCSV.setGeometry(QtCore.QRect(210, 25, 261, 21))
        self.le_weightFromCSV.setObjectName(_fromUtf8("le_weightFromCSV"))
        self.tabWidget.addTab(self.tb_main, _fromUtf8(""))
        self.tb_weight = QtGui.QWidget()
        self.tb_weight.setObjectName(_fromUtf8("tb_weight"))
        self.tbl_setWeights = QtGui.QTableWidget(self.tb_weight)
        self.tbl_setWeights.setGeometry(QtCore.QRect(10, 10, 491, 361))
        self.tbl_setWeights.setAlternatingRowColors(True)
        self.tbl_setWeights.setColumnCount(2)
        self.tbl_setWeights.setObjectName(_fromUtf8("tbl_setWeights"))
        self.tbl_setWeights.setRowCount(0)
        self.pb_submitWeight = QtGui.QPushButton(self.tb_weight)
        self.pb_submitWeight.setGeometry(QtCore.QRect(420, 380, 81, 23))
        self.pb_submitWeight.setObjectName(_fromUtf8("pb_submitWeight"))
        self.tabWidget.addTab(self.tb_weight, _fromUtf8(""))

        self.retranslateUi(rkValidation)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(rkValidation)

    def retranslateUi(self, rkValidation):
        rkValidation.setWindowTitle(_translate("rkValidation", "Validation Tool 1.1 - Copyright (C) 2014 René Kopeinig", None))
        self.pb_close.setToolTip(_translate("rkValidation", "<html><head/><body><p>Close Validation tool</p></body></html>", None))
        self.pb_close.setText(_translate("rkValidation", "Close", None))
        self.pb_help.setToolTip(_translate("rkValidation", "<html><head/><body><p>Shows you basic information about the validation tool. For more specific questions, please contact the developer of this tool (rkopeinig@conabio.gob.mx).</p></body></html>", None))
        self.pb_help.setText(_translate("rkValidation", "Help", None))
        self.gb3.setTitle(_translate("rkValidation", "Execute Validation", None))
        self.pb_validate.setToolTip(_translate("rkValidation", "<html><head/><body><p>Executes the validation. Make sure all parameters above are set.</p></body></html>", None))
        self.pb_validate.setText(_translate("rkValidation", "Validate", None))
        self.gb2.setTitle(_translate("rkValidation", "Set Output (optional)", None))
        self.pb_outFolder.setToolTip(_translate("rkValidation", "<html><head/><body><p>Set output file. If you do not set any output, it will be named after your input file plus the suffix &quot;_validation.csv&quot;</p></body></html>", None))
        self.pb_outFolder.setText(_translate("rkValidation", "Select Output File", None))
        self.cb_useWeight.setText(_translate("rkValidation", "Usage of Weight", None))
        self.gb1.setTitle(_translate("rkValidation", "Set Input", None))
        self.pb_uploadShape.setToolTip(_translate("rkValidation", "<html><head/><body><p>Select either ESRI Shapefile (.shp) or ESRI Shapefile attribute format (.dbf)</p></body></html>", None))
        self.pb_uploadShape.setText(_translate("rkValidation", "Select Input File", None))
        self.lb_preColNr.setText(_translate("rkValidation", "Predicted", None))
        self.lb_refColNr.setText(_translate("rkValidation", "Reference", None))
        self.rb_weight.setText(_translate("rkValidation", "Weight-based", None))
        self.rb_noweight.setText(_translate("rkValidation", "Normal", None))
        self.gb4.setTitle(_translate("rkValidation", "Area Selection for Weight-based Validation", None))
        self.pb_selectWeight.setToolTip(_translate("rkValidation", "<html><head/><body><p>Select either ESRI Shapefile (.shp) or ESRI Shapefile attribute format (.dbf)</p></body></html>", None))
        self.pb_selectWeight.setText(_translate("rkValidation", "Set Area manually from List", None))
        self.pb_selectWeight_csv.setToolTip(_translate("rkValidation", "<html><head/><body><p>Select either ESRI Shapefile (.shp) or ESRI Shapefile attribute format (.dbf)</p></body></html>", None))
        self.pb_selectWeight_csv.setText(_translate("rkValidation", "Load Area from CSV file", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tb_main), _translate("rkValidation", "Validation", None))
        self.tbl_setWeights.setToolTip(_translate("rkValidation", "<html><head/><body><p>Displays label (class) and the weight (area) per class</p></body></html>", None))
        self.tbl_setWeights.setSortingEnabled(True)
        self.pb_submitWeight.setText(_translate("rkValidation", "Submit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tb_weight), _translate("rkValidation", "Area", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    rkValidation = QtGui.QDialog()
    ui = Ui_rkValidation()
    ui.setupUi(rkValidation)
    rkValidation.show()
    sys.exit(app.exec_())

