# -*- coding: utf-8 -*-
"""
/***************************************************************************
 validation
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
# Import the code for the dialog
from validationdialog import validationDialog
import os.path


class validation:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'validation_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = validationDialog(self.iface)

    def initGui(self):
        # Create action that will start plugin configuration
        icon = QIcon(os.path.dirname(__file__) + "/icons/rk_validation_small.png")
        self.action = QAction(
            icon,u"Validation Tool", self.iface.mainWindow())
        #self.action = QAction(
        #    QIcon(":/plugins/validation/madmex_small.png"),
        #    u"Validation Tool", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Validation Tool", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Validation Tool", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
