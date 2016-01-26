# create layer
vl = QgsVectorLayer("Point", "temporary_points", "memory")
pr = vl.dataProvider()

# changes are only possible when editing the layer
vl.startEditing()
# add fields

# add a feature
fet = QgsFeature()
fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(10,10)))
pr.addFeatures([fet])

# commit to stop editing the layer
vl.commitChanges()

# update layer's extent when new features have been added
# because change of extent in provider is not propagated to the layer
vl.updateExtents()

# add layer to the legend
QgsMapLayerRegistry.instance().addMapLayer(vl)