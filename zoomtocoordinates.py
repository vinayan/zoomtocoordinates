# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZoomToCoordinates
                                 A QGIS plugin
 Zoom,Pan and Highlight Entered Coordinates
                              -------------------
        begin                : 2013-04-10
        copyright            : (C) 2013 by Vinayan Parameswaran
        email                : vinayan123@gmail.com
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
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsRubberBand
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from zoomtocoordinatesdialog import ZoomToCoordinatesDialog


class ZoomToCoordinates:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/zoomtocoordinates"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/zoomtocoordinates_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ZoomToCoordinatesDialog()
        self.dlg.setWindowModality(QtCore.Qt.NonModal)
        self.dlg.setParent(self.iface.mainWindow(),QtCore.Qt.Dialog)
        #self.dlg = QtGui.QMainWindow(self.iface.mainWindow(), QtCore.Qt.Dialog)
        
        #validations
        validator = QtGui.QDoubleValidator()
        lEditX = self.dlg.ui.mTxtX
        lEditY = self.dlg.ui.mTxtY       
        lEditX.setValidator(validator)
        lEditY.setValidator(validator)
        
        #todo - set scale as a spinbox
        self.scale = 100
        self.rubberBand = QgsRubberBand(iface.mapCanvas(),QGis.Point)
        self.rubberBand.setColor(Qt.red)
        #self.rubberBand.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
        self.rubberBand.setIconSize(7)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/zoomtocoordinates/icon.png"),
            u"ZoomToCoordinates", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        
        QObject.connect(self.dlg.ui.mActionZoomTo, SIGNAL("activated()"), self.zoom)
        QObject.connect(self.dlg.ui.mActionPan, SIGNAL("activated()"), self.pan)
        QObject.connect(self.dlg.ui.mActionFlash, SIGNAL("activated()"), self.flash)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&ZoomToCoordinates", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&ZoomToCoordinates", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = 1
        #result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
            
    def zoom(self):
		print "zoom button clicked!"
		x = self.dlg.ui.mTxtX.text()
		y = self.dlg.ui.mTxtY.text()
		
		if x.isEmpty():
			return
		
		if y.isEmpty():
			return
			
		print x + "," + y
		
		rect = QgsRectangle(float(x)-self.scale,float(y)-self.scale,float(x)+self.scale,float(y)+self.scale)
		self.canvas.setExtent(rect)
		pt = QgsPoint(float(x),float(y))
		self.highlight(pt)
		self.canvas.refresh()
		
    def pan(self):
		print "pan button clicked!"
		x = self.dlg.ui.mTxtX.text()
		y = self.dlg.ui.mTxtY.text()
		
		if x.isEmpty():
			return
		
		if y.isEmpty():
			return
		
		print x + "," + y
		
		canvas = self.canvas
		currExt = canvas.extent()
		
		canvasCenter = currExt.center()
		dx = float(x) - canvasCenter.x()
		dy = float(y) - canvasCenter.y()
		
		xMin = currExt.xMinimum() + dx
		xMax = currExt.xMaximum() + dx
		yMin = currExt.yMinimum() + dy
		yMax = currExt.yMaximum() + dy
		
		newRect = QgsRectangle(xMin,yMin,xMax,yMax)
		canvas.setExtent(newRect)
		canvas.refresh()
		
    def flash(self):
		print "flash button clicked!"
		
		x = self.dlg.ui.mTxtX.text()
		y = self.dlg.ui.mTxtY.text()
		
		if x.isEmpty():
			return
		
		if y.isEmpty():
			return
			
    def highlight(self,point):
		print "highlighting.."
		rb = self.rubberBand
		rb.reset(QGis.Point)
		rb.addPoint(point)
		QTimer.singleShot(500,self.resetRubberbands)
    
    def resetRubberbands(self):
		print "resetting rubberbands.."
		self.rubberBand.reset()
		print "completed resetting.."
		
