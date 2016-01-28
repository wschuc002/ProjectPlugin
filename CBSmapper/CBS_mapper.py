# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CBSmapper
                                 A QGIS plugin
 Can map CBS demographic data
                              -------------------
        begin                : 2016-01-25
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Geodetic Engineers of Utrecht
        email                : saxoriko@gmail.com
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
#Importing the packages that are used
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
from CBS_mapper_dialog import CBSmapperDialog # Import the code for the dialog
from qgis.core import *
import os.path
# Initialize Qt resources from file resources.py
import resources


class CBSmapper:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CBSmapper_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = CBSmapperDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&CBS Mapper')       
        self.toolbar = self.iface.addToolBar(u'CBSmapper')
        self.toolbar.setObjectName(u'CBSmapper')
        
        #clearing the export line
        self.dlg.export_line.clear() 
        #Connecting several push buttons with functions
        self.dlg.pushButton_addWFS_gemeenten.clicked.connect(self.add_WFS_gemeenten)
        self.dlg.pushButton_addWFS_buurten.clicked.connect(self.add_WFS_buurten)

        self.dlg.pushButton_refresh.clicked.connect(self.refresh_layers)        
        
        self.dlg.pushButton_showSelect.clicked.connect(self.selectfeatures)
        self.dlg.pushButton_browseGjsonSelect.clicked.connect(self.select_output_file_gjson) 
        self.dlg.pushButton_exportGjsonSelect.clicked.connect(self.write_gjson)
        
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CBSmapper', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CBSmapper/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'The Mapper'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&CBS Mapper'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def add_WFS_gemeenten(self):
        """Add gemeenten WFS layer to QGIS map canvas."""
         
        # Load the wfs
        url = "http://geodata.nationaalgeoregister.nl/wijkenbuurten2014/wfs?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=wijkenenbuurten2014:gemeenten2014&SRSNAME=EPSG:28992" 
        self.iface.addVectorLayer(url, "gemeenten2014", "WFS")        
        
        self.refresh_layers()

    def add_WFS_buurten(self):
        """Add buurten WFS layer to QGIS map canvas."""
         
        # Load the wfs
        #url = "https://geodata.nationaalgeoregister.nl/wijkenbuurten2014/wfs?version=1.0.0&request=getcapabilitieswijkenbuurten2014:cbs_buurten_2014" 
        url = "https://geodata.nationaalgeoregister.nl/wijkenbuurten2014/wfs?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=wijkenbuurten2014:cbs_buurten_2014&SRSNAME=EPSG:28992&BBOX=0,300000,300000,600000"               
        self.iface.addVectorLayer(url, "buurten2014", "WFS")
        
        self.refresh_layers()

    def refresh_layers(self):
        """Refresh layers and field names so that they are recognized in the plugin"""        
        
        # select layer
        layer = self.iface.activeLayer()
   
        # Get layers that are loaded in QGIS.        
        layers = self.iface.legendInterface().layers()  
        # create a list with layer names        
        layer_list = []                                 
        for layer in layers:                            
            layer_list.append(layer.name())
        # Clear the old layer names in the combobox             
        self.dlg.comboBox_addLayer.clear()
        # Add the new layer names to the combobox
        self.dlg.comboBox_addLayer.addItems(layer_list) 
        
        # Get the active layer in QGIS
        activelayer = self.iface.activeLayer()  
        # Get the fieldnames of the layer
        fields = activelayer.pendingFields()
        field_names = []        
        field_names = [field.name() for field in fields]
        # Clear the old fieldnames in the combobox                
        self.dlg.comboBox_selectAtt.clear()
        # Add the new field names to the combobox
        self.dlg.comboBox_selectAtt.addItems(field_names)       

    def selectquery(self, query):
        """Selecting the query."""               
        
        layer = self.iface.activeLayer()
        query_str = str(query)
        
        #Create a Expression
        expr = QgsExpression(query_str)
        selected = layer.getFeatures(QgsFeatureRequest(expr))
        
        #Build a list of feature Ids from the result
        ids = []
        for i in selected:
            ids.append(i.id())
        
        #Select features with the ids
        layer.setSelectedFeatures( ids )

    def selectfeatures(self):
        """Selecting the features."""   
        
        # get fieldname
        attribute = self.dlg.comboBox_selectAtt
        fieldname = str(attribute.currentText())
        
        # get query
        query_line = self.dlg.query_line
        query = str(query_line.toPlainText())
        
        combined_query = "%s %s" % (fieldname, query)
        #print combined_query
        self.selectquery(combined_query)
        

    def select_output_file_gjson(self):
        """Selects the output GeoJSON file from QGIS GUI."""
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.gjson')
        self.dlg.export_line.setText(filename)

    def write_gjson(self):
        """Writes the output GeoJSON file from QGIS GUI."""
        # getting the selected layer
        layer = self.iface.activeLayer()
        # getting the path from the path line
        JSONpath = self.dlg.export_line.text()
        # write layer selection to geojson with location of choice (export line)
        QgsVectorFileWriter.writeAsVectorFormat(layer, JSONpath, "utf-8", None, "GeoJSON", onlySelected=True)


    def run(self):
        """Run method that shows the dialog"""                
        self.dlg.show()     