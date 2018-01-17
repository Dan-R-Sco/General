import arcpy, os, humanize, glob

def write_log(text,file):
    f = open(file,'a')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return

output = r'X:\daniel.scott\sizemxd6.txt' #arcpy.GetParameterAsText(0)

mxd = arcpy.mapping.MapDocument(r"G:\08_TiramisuProjects\W1612\Workspace\Consolidated GIS\TGTA_W1612_ConsolidatedGISPhase3_27112017.mxd")
df = arcpy.mapping.ListDataFrames(mxd)

write_log("This report summarizes the names of all map documents and data frames within " + mxd.filePath +  "\n",output)
write_log("Date: " + str(datetime.datetime.today().strftime("%d %B, %Y")) + "\n",output)

for d in df:
    write_log("Data Frame: " + d.name, output)
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    for lyr in layers:
        try:
            if lyr.supports("dataSource"):
                lname = lyr.name
                print "lname: " + lname
                datasource = lyr.dataSource
                wspath = lyr.workspacePath
                if datasource.endswith('.shp'):
                    stringwspath = str(wspath).replace("\\", '/')
                    path = stringwspath + "/"
                    print "Path: " + path
                    for shp in glob.glob(os.path.join(path,'{0}.*').format(lname)):
                        shp = str(shp).replace("\\", '/')
                        print "stripped " + stripshp
                        try:
                            size = os.stat(shp).st_size
                            print "size of shp " + stripshp + " is " + humanize.naturalsize(size)
                        except:
                            print "unable to access size of " + shp
                else:
                    pass
            else:
                pass
        #print "File size: " + humanize.size
        except:
            print "Unable to analyse size for " + lname.encode('utf-8')