# -*- coding: utf-8 -*-

layer = iface.activeLayer()


#Get gemeenten without null value in name:
expr = QgsExpression('aantal_inwoners > 200000')
selected = layer.getFeatures( QgsFeatureRequest( expr ) )

#Build a list of feature Ids from the result
#ids = [i.id() for i in selected]
ids = []
for i in selected:
    ids.append(i.id())

#Select features with the ids
layer.setSelectedFeatures( ids )

# export to geojson
name = "inwoners"
JSONpath = "/home/user/git/ProjectPlugin/data/%s.geojson" % name
QgsVectorFileWriter.writeAsVectorFormat(layer, JSONpath, "utf-8", None, "GeoJSON", onlySelected=True)

