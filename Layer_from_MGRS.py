##Kaynak_Tablo=table
##Yeni_Katman=output vector
##MGRS_Alani=field Kaynak_Tablo

import pymgrs
from qgis.core import *

layer = processing.getObject(Kaynak_Tablo)
features = layer.getFeatures()

mgrs_field_index = layer.fieldNameIndex(MGRS_Alani)

fields = layer.fields()
for field in fields:
    progress.setText(str(field))

# create target layer
crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
writer = processing.VectorWriter(Yeni_Katman, None, fields, QGis.WKBPoint, crs)

outFeat = QgsFeature()

for feature in features:
    attrs = feature.attributes()
    #progress.setText(str(attrs))    
    
    #x = float(attrs[x_field_index])
    #y = float(attrs[x_field_index])
        
    try:
        ll = pymgrs.MGRStoLL(attrs[mgrs_field_index])
        #progress.setInfo(str(ll))
        
        x = float(ll['lon'])
        y = float(ll['lat'])
    except:
        continue
    
    pt = QgsPoint(x, y)
    
    outFeat.setGeometry(QgsGeometry.fromPoint(pt))
    outFeat.setAttributes(attrs)
    writer.addFeature(outFeat)
    
del writer
