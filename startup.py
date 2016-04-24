import qgis
import pymgrs
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform

iface = qgis.utils.iface

iface.mainWindow().statusBar().show()


sourceCrs = QgsCoordinateReferenceSystem(iface.mapCanvas().mapRenderer().destinationCrs().postgisSrid())
destCrs = QgsCoordinateReferenceSystem(4326)
xform = QgsCoordinateTransform(sourceCrs, destCrs) #you can also do reverse convertion

def updateSourceCrs():
	global sourceCrs
	global destCrs
	global xform
	sourceCrs = QgsCoordinateReferenceSystem(iface.mapCanvas().mapRenderer().destinationCrs().postgisSrid())
	destCrs = QgsCoordinateReferenceSystem(4326)
	xform = QgsCoordinateTransform(sourceCrs, destCrs) #you can also do reverse convertion



# bind signal
def showCoords(xy):
	point = xform.transform(xy)	
	iface.mainWindow().statusBar().showMessage(pymgrs.LLtoMGRS(point.y(), point.x()))	

# init
#showCoords(qgis.core.QgsPoint(0, 0))

#iface.mapCanvas().mapRenderer().destinationCrs().srsid()
iface.mapCanvas().xyCoordinates.connect(showCoords)
iface.mapCanvas().destinationCrsChanged.connect(updateSourceCrs)
