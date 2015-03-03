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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load validation class from file validation
    from validation import validation
    return validation(iface)
