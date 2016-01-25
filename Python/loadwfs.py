#qgis.utils.iface.addVectorLayer(
#"http://geodata.nationaalgeoregister.nl/wijkenbuurten2014/wfs?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=wijkenenbuurten2014:gemeenten2014&SRSNAME=EPSG:28992",
#"gemeenten2014",
#"WFS")


layer = iface.activeLayer()
#
#for f in layer.getFeatures():
#  print f['gemeentenaam']

#layer.setSubsetString('gemeentenaam IS NOT NULL')


exp = QgsExpression('gemeentenaam IS NOT NULL')
request = QgsFeatureRequest(exp)

#for feature in layer.getFeatures(request):
#    print feature['gemeentenaam']


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