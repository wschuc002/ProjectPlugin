layer = qgis.utils.iface.activeLayer()  
fields = layer.pendingFields()   
field_names = [field.name() for field in fields]        
print field_names
#self.dlg.comboBox_selectAtt.addItems(field_names) #Toegevoegd!
        
        
