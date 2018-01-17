import arcpy, os, humanize
from arcpy import env
def write_log(text,file):
    f = open(file,'a')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return
output = r'X:\daniel.scott\mxd6.txt'

mxd = arcpy.mapping.MapDocument(r"G:\08_TiramisuProjects\W1612\Workspace\Consolidated GIS\TGTA_W1612_ConsolidatedGISPhase3_27112017.mxd")  # Uses your currently open MXD
df = arcpy.mapping.ListDataFrames(mxd, '')[0] # Chooses the first dataframe

env.workspace = 'c:/temp/python'
write_log("-------------------------------------------------------------------",output)
write_log("                         MAPDOCUMENT: " + os.path.basename(mxd.filePath), output)
write_log("Path:  " + mxd.filePath, output)
write_log("Last saved:           " + str(mxd.dateSaved),output)

write_log("This report summarizes the names of all map documents and data frames within " + mxd.filePath +  "\n",output)
write_log("Date: " + str(datetime.datetime.today().strftime("%d %B, %Y")) + "\n",output)

# Determine if the data source exists within the data frames/map document
for df in arcpy.mapping.ListDataFrames(mxd):
    write_log("Data frame name: " + df.name, output)
    write_log("Data frame spatial reference system: " + df.spatialReference.name, output)
    layerlist = arcpy.mapping.ListLayers(mxd, '', df)
    layerlistvalue = str(len(layerlist))
    write_log("There are " + layerlistvalue + " layers in this mxd", output)
    brknMXD = arcpy.mapping.ListBrokenDataSources(mxd)
    if len(brknMXD) == 0:
        brknMXDValue = "None"
    else:
        brknMXDValue = "A total of " + str(len(brknMXD)) + " broken data source(s)."
    write_log("Broken Data Sources in this MXD:  " + brknMXDValue + "\n", output)
    write_log("The list of broken layers are:  ", output)
    layersskip = []

    for brklayer in brknMXD:
        write_log("\t \t Broken layer: " + brklayer.name.encode('utf-8') + "\n", output)
    write_log("Spatial reference analysis results: ", output)
    unkwn = 0
    for layer in layerlist:
        if layer in brknMXD:
            pass
        elif layer.isGroupLayer: #add code to count lyrs in this layer group
            pass
        else:
            try:
                desc = arcpy.Describe(layer)
                srname = desc.spatialReference.name
                if df.spatialReference.name == srname:
                    pass
                # fails with layers with broken data sources
                elif srname == 'Unknown':
                    unkwn = unkwn + 1
                    write_log('\t' + '\t' + "Layer name: " + layer.name.encode('utf-8') + " has an unknown spatial projection",output)
                elif srname == None:
                    unkwn = unkwn + 1
                    write_log('\t' + '\t' + "Layer name: " + layer.name.encode('utf-8') + ", doesn't have a spatial projection, how can this be used?", output)
                else:
                    unkwn = unkwn + 1
                    write_log('\t' + '\t' + "Layer name: " + layer.name.encode('utf-8') + " is in a different spatial reference to the dataframe: " + srname,output)
            except:
                write_log("Unable to access spatial reference for " + layer.name.encode('utf-8'),output)
                pass
    write_log("\n + Total layers with the wrong spatial projection: " + str(unkwn) + " layers", output)

    write_log("---------------------------------------------------------------------", output)