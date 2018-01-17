import arcpy, os, humanize

def convertSize(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)


for d in df:
    print "Data Frame: " + d.name
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    for lyr in layers:
        try:
            lname = lyr.name
            datasource = lyr.dataSource
            wspath = lyr.workspacePath

            print "Layer Name: " + lname
            print "Data Source: " + datasource
            print "Workspace Path: " + wspath
            #print "File size: " + humanize.size
            try:
                statinfo = os.stat(wspath)
                size = statinfo.st_size
                print "Size: " + size
            except:
                pass

        except:
            pass