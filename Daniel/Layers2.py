import arcpy, os
from stat import ST_SIZE

mxd = arcpy.mapping.MapDocument("C:\Users\daniel.scott\Desktop\Untitled.mxd")

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        print os.path.getsize(lyr.dataSource)