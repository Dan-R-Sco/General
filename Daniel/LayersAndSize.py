import arcpy, os, humanize

def write_log(text,file):
    f = open(file,'a')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return

def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size

log = r'X:\daniel.scott\mxdsize.txt' #name of log file

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

for lyr in arcpy.mapping.ListLayers(mxd, "",df):
    desc = arcpy.Describe(lyr)
    try:
        if lyr.dataType == "FeatureClass":
            try:
                if desc.dataElement.dataType == "FeatureClass":
                    print("Feature class:      " + desc.dataElement.catalogPath)
                    write_log("Feature class:      " + desc.dataElement.catalogPath,log)
                    print("Feature class Type: " + desc.featureClass.featureType)
                    write_log("Feature class Type: " + desc.featureClass.featureType, log)

                if lyr.supports("DATASOURCE"):
                    dataSource = lyr.dataSource
                    os.path.realpath = dataSource
                    filesize = os.path.getsize(dataSource)
                    write_log("layer name type is: " + lyr.name + ", layer directory {0}".format(dataSource) + ", layer is " + humanize.filesize.encode('utf-8') , log)

                elif desc.dataElement.dataType == None:
                    print(desc.name + " has no data type")



        else:
            print("Not a regular feature class")
            pass




    # add shp file
        #if lyr.dataType == "ShapeFile":
            #try:
            #fullPath = os.path.join(root, fileName)
            #lyrpath = arcpy.mapping.Layer(fullPath)
