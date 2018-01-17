import arcpy, os, humanize, glob

def write_log(text,file):
    f = open(file,'a')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return

output = r'X:\daniel.scott\sizemxd6.txt' #arcpy.GetParameterAsText(0)

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)

write_log("This report summarizes the names of all map documents and data frames within " + mxd.filePath +  "\n",output)
write_log("Date: " + str(datetime.datetime.today().strftime("%d %B, %Y")) + "\n",output)

for d in df:
    write_log("Data Frame: " + d.name, output)
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    for lyr in layers:
        sizelist = []
        sumsize = sum(sizelist)
        print sumsize
        try:
            if lyr.supports("dataSource"):
                lname = lyr.name
                datasource = lyr.dataSource
                wspath = lyr.workspacePath
                stringwspath = str(wspath).replace("\\",'/')
                path = stringwspath
                for shp in glob.glob(os.path.join(path,'{0}.*').format(lname)):
                    total = 0
                    print shp
                    try:
                        size = os.stat(shp).st_size
                        total = total + size
                        write_log("Size: " + size, output)
                        try:
                            write_log("total accumlative shp size: " + total, output)
                        except:
                            write_log("Unable to calculate cumulative size for " + shp, output)
                    except:
                        write_log("Unable to access the size of " + shp,output)
                write_log("Layer Name: " + lname, output)
                print "Layer Name: " + lname
                write_log("Data Source: " + datasource, output)
                print "Data Source: " + datasource
                write_log("Workspace Path: " + wspath,output)
                print "Workspace Path: " + wspath
                try:

                    statinfo = os.stat(wspath)
                    size = statinfo.st_size
                    hsize = humanize.naturalsize(size)
                    write_log("Size: " + hsize, output)
                    print "Size: " + hsize
                    sizelist.append(hsize)
                except:
                    write_log("Unable to analyse size for " + lname, output)
        #print "File size: " + humanize.size
        except:
            write_log("Unable to analyse size for " + lname, output)

    write_log("the sum of the number of files in your mxd is {0}".format(sumsize), output)