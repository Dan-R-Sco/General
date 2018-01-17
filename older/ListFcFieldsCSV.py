import arcpy
from arcpy import env
import os


# For each field in the Hospitals feature class, print
#  the field name, type, and length.

arcpy.env.workspace = "C:\Users\daniel.scott\AppData\Roaming\ESRI\Desktop10.4\ArcCatalog\ADMIN_NDP@10.70.2.155@NDP_EGDB_20170105A.sde\NDP_EGDB_20170105A.ADMIN_NDP.Template"
fclist = arcpy.ListFeatureClasses()
for fc in fclist:
    print "Feature class name = " + fc[29:]
    fieldlist = arcpy.ListFields(fc)
    for field in fieldlist:
        print("Field name = '{0}', Data type = '{1}', length of field = '{2}'".format(field.name, field.type, field.length))

