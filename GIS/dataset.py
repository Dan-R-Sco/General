import arcpy

arcpy.env.workspace = r'Database Connections\admin_ndp@srv-sql03@egdtesting.sde'

fcList = []

for dataseti in arcpy.ListDatasets():
    for fc in arcpy.ListFeatureClasses("*", "ALL", dataseti):
        fcList.append(fc)
        print fc

print fcList
