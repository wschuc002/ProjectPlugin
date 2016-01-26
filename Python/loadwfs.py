# loadwfs.py

# Load the wfs
url = "http://geodata.nationaalgeoregister.nl/wijkenbuurten2014/wfs?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=wijkenenbuurten2014:gemeenten2014&SRSNAME=EPSG:28992" 
qgis.utils.iface.addVectorLayer(url, "gemeenten2014", "WFS")

# select gemeenten layer
layer = iface.activeLayer()

#Get gemeenten without null value in name:
expr = QgsExpression('gemeentenaam IS NOT NULL')
gemeenten_notnull = layer.getFeatures( QgsFeatureRequest( expr ) )

#Build a list of feature Ids from the result
ids = [i.id() for i in gemeenten_notnull]

#Select features with the ids
layer.setSelectedFeatures( ids )

# write geojson
JSONpath = "/home/user/git/ProjectPlugin/data/gemeenten_2014.geojson"
QgsVectorFileWriter.writeAsVectorFormat(layer, JSONpath, "utf-8", None, "GeoJSON", onlySelected=True)

# delete gemeenten wfs from qgis
QgsMapLayerRegistry.instance().removeMapLayer(layer.id())

# add gemeenten geojson to qgis
iface.addVectorLayer(JSONpath, "gemeenten_2014", "ogr")


