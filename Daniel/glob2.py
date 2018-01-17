import arcpy, os, glob, humanize
 ##need to add to search for dbf files as well idea here: https://gis.stackexchange.com/questions/174323/retrieving-size-of-shapefile-in-arcpy

def write_log(text,file):
    f = open(file,'a')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return
output = r'X:\daniel.scott\sizemxd2.txt' #arcpy.GetParameterAsText(0)
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)
write_log("This report summarizes the names of all map documents and data frames within " + mxd.filePath +  "\n",output)
write_log("Date: " + str(datetime.datetime.today().strftime("%d %B, %Y")) + "\n",output)
for d in df:
    write_log("Data Frame: " + d.name, output)
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    for lyr in layers:

        try:
            lname = lyr.name
            datasource = lyr.dataSource
            wspath = lyr.workspacePath
            write_log("Layer Name: " + lname, output)
            print "Layer Name: " + lname
            write_log("Data Source: " + datasource, output)
            strwspath = str(wspath)
            wspatha = wspath.replace("\\",'/')
            shpsizels = []
            shapefiles = glob.glob(os.path.join(wspatha,"{0}*").format(lname))
            for shapefile in shapefiles:
                strshpfile = str(shapefile)
                stripshp = strshpfile.replace("\\",'/')
                print stripshp
                try:
                    size = os.stat(stripshp).st_size
                    print size
                    shpsizels.append(size)
                except:
                    pass
            tot = sum(int(shpsizels))

        except:
            pass

b = sum(shpsizels)

print "shp size ls has the following values: " + str(b)

print "XXXX" + str(shpsizels)
total_size = sum(shpsizels)
humansize = humanize.naturalsize(total_size)
print " the total size for " + lname + " is " + humansize