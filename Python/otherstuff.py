#
#for f in layer.getFeatures():
#  print f['gemeentenaam']

#layer.setSubsetString('gemeentenaam IS NOT NULL')


exp = QgsExpression('gemeentenaam IS NOT NULL')
request = QgsFeatureRequest(exp)

#for feature in layer.getFeatures(request):
#    print feature['gemeentenaam']

