# -*- coding: utf-8 -*-

#For use with ArcGIS in Windows. Compatibility with other platforms not tested.
#Writes to a text file some basic Layer information (Path, Layer Name, Spatial Reference)

# reference
# http://gis.stackexchange.com/questions/52893/getting-unicode-encode-error-in-arcpy-python-script

from __future__ import print_function
import codecs
import os.path, time
import arcpy

#os.path.basename("C:\workdir\project1")
mxd=arcpy.mapping.MapDocument("CURRENT")
dataframes=arcpy.mapping.ListDataFrames(mxd)

filename=os.path.basename(mxd.filePath)

failCheck=None

#Open file to write information into
with codecs.open("C:\Users\daniel.scott\Documents" + filename + "PythonTest.txt",
                 "w",
                encoding="utf-8") as f:
    print("Path;LayerGroup;LayerName;SpatialReference;ModificationTime", file=f)
    #Start the for loop that goes through all the layers in the .mxd
    #This for loop can be taken out of the "with" part of the code
    for dataframe in dataframes:
        for lyr in arcpy.mapping.ListLayers(mxd,"",dataframe):
            #From here on the code could do anything, you can delete it or change it
            if not lyr.isGroupLayer:
                try:
                    layerPath=arcpy.Describe(lyr).catalogPath
                    layerSpatialRef=arcpy.Describe(lyr).spatialReference.Name
                    layerGroupName=arcpy.Describe(lyr).nameString
                    layerName=layerGroupName.rsplit('\\',1)
                    modDate=None
                    if layerPath.find(".gdb") == -1:
                        modDate=os.path.getmtime(layerPath)
                    # print(layerPath.find(".gdb"))
                except:
                    print("FAIL;FAIL;FAIL;FAIL;FAIL", file=f)
                    failCheck=True
                    pass
                print(layerPath + ";" + layerGroupName +";" + layerName[-1] + ";" + layerSpatialRef + ";" + time.ctime(modDate), file=f)
             #Until here
if failCheck:
	print("Couldn't read information from all layers. Check if Basemaps or Annotation \
	 layers are present in the map, and ignore their warnings in the output file")
