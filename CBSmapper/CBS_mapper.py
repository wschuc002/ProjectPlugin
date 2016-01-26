# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CBSmapper
                                 A QGIS plugin
 Can map CBS demographic data
                              -------------------
        begin                : 2016-01-25
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Geodetic engeneers
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtGui import QFileDialog                  #Toegevoegd!   
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from CBS_mapper_dialog import CBSmapperDialog
import os.path


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
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CBSmapper')
        self.toolbar.setObjectName(u'CBSmapper')
        
        
        self.dlg.lineEdit.clear()                                       #Toegevoegd
        self.dlg.pushButton_exportSelect.clicked.connect(self.select_output_file)    #Toegevoegd       
        

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


    def select_output_file(self):                                                           #Toegevoegd
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.txt') #Toegevoegd
        self.dlg.lineEdit.setText(filename)                                                 #Toegevoegd


    def run(self):
        """Run method that performs all the real work"""
        layers = self.iface.legendInterface().layers()  #Toegevoegd!
        layer_list = []                                 #Toegevoegd!
        for layer in layers:                            #Toegevoegd!
            layer_list.append(layer.name())             #Toegevoegd!
        self.dlg.comboBox_addLayer.addItems(layer_list) #Toegevoegd!
        
        self.dlg.comboBox_selectAtt.addItems(layer_list) #Toegevoegd!
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            filename = self.dlg.lineEdit.text()                             #Toegevoegd!
            output_file = open(filename, 'w')                               #Toegevoegd!
            
            selectedLayerIndex = self.dlg.comboBox_addLayer.currentIndex()           #Toegevoegd!
            selectedLayer = layers[selectedLayerIndex]                      #Toegevoegd!
            fields = selectedLayer.pendingFields()                          #Toegevoegd!
            fieldnames = [field.name() for field in fields]                 #Toegevoegd!
            
            for f in selectedLayer.getFeatures():                           #Toegevoegd!
                line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'   #Toegevoegd!
                unicode_line = line.encode('utf-8')                         #Toegevoegd!
                output_file.write(unicode_line)                             #Toegevoegd!
            output_file.close()                                             #Toegevoegd!
