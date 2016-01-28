# graduated

import os
os.chdir("/home/user/git/ProjectPlugin/Python")
print os.getcwd()

# select gemeenten layer
layer = iface.activeLayer()

layer.loadSldStyle("bev_dichtheid.sld")
#iface.mapCanvas().refresh()
layer.triggerRepaint()
