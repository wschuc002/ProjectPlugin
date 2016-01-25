# -*- coding: utf-8 -*-


## select gemeentes with delf in the name
#exp = QgsExpression('gemeentenaam ILIKE \'%Delf%\'')
#request = QgsFeatureRequest(exp)

#for feature in layer.getFeatures(request):
#    print feature['gemeentenaam']


layer = iface.activeLayer()

exp = QgsExpression('aantal_inwoners > 200000')
request = QgsFeatureRequest(exp)

for feature in layer.getFeatures(request):
    inwoners = feature['aantal_inwoners']
    #if inwoners > 200000:
    print feature['gemeentenaam']

