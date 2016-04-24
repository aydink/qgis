##Kaynak_Tablo=table
##Yeni_Katman=output vector
##MGRS_Alani=field Kaynak_Tablo

import pymgrs

from qgis.core import *
from PyQt4.QtCore import *

layer = processing.getObject(Kaynak_Tablo)
features = layer.getFeatures()

mgrs_field_index = layer.fieldNameIndex(MGRS_Alani)

fields = layer.fields()

fields.append(QgsField("xkoor", QVariant.Double))
fields.append(QgsField("ykoor", QVariant.Double))

#xkoor_index = layer.fieldNameIndex(xkoor)
#ykoor_index = layer.fieldNameIndex(ykoor)

for field in fields:
    progress.setText(str(field))



# create target layer
crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
writer = processing.VectorWriter(Yeni_Katman, None, fields, QGis.WKBPoint, crs)


outFeat = QgsFeature()

for feature in features:
    attrs = feature.attributes()
    #progress.setText(str(attrs))
    
    attrs.append(QgsField("xkoor", QVariant.Double))
    attrs.append(QgsField("ykoor", QVariant.Double))
    
    #x = float(attrs[x_field_index])
    #y = float(attrs[x_field_index])
        
    try:
        mgrs = pymgrs.MGRStoLL(str(attrs[mgrs_field_index]))
        #progress.setInfo(str(mgrs))
        
        x = mgrs['lon']
        y = mgrs['lat']
        
        xkoor_index = len(attrs)
        ykoor_index = xkoor_index + 1 
        
        attrs["xkoor"] = x
        attrs["ykoor"] = y
        
    except:
        continue
    
    pt = QgsPoint(x, y)
    
    outFeat.setGeometry(QgsGeometry.fromPoint(pt))
    outFeat.setAttributes(attrs)
    writer.addFeature(outFeat)
    
del writer

