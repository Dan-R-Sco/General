import arcpy,os
mxd = arcpy.mapping.MapDocument("C:\Users\daniel.scott\Desktop\TGTA_W1612_ConsolidatedGISPhase1_31102017.mxd") #input path to mxd
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.isRasterLayer == True:
        lyrsource = lyr.dataSource
        filesize = os.stat(lyrsource).st_size
        print "raster layer: " + lyr.name + " Source: " + lyr.dataSource + " file size: " + str(filesize)