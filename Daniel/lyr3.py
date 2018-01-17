import arcpy, os

# Update the following path with the folder you want to inspect
path = r"C:\Users\daniel.scott\Desktop"
# Update the .csv file name below
f = open('2004_Test.csv', 'w')
f.write("Type, File Path, Layer, Broken Path" + "\n")
for root, dirs, files in os.walk(path):
    for fileName in files:
        basename, extension = os.path.splitext(fileName)
        # Write the information for all .mxd's with broken data sources
        if extension == ".mxd":
            fullPath = os.path.join(root, fileName)
            mxd = arcpy.mapping.MapDocument(fullPath)
            brknMXD = arcpy.mapping.ListBrokenDataSources(mxd)
            try:

                for brknItem in brknMXD:
                    f.write("MXD, " + fullPath + ", " + brknItem.name)
                    # Test to see if the data type is able to return a dataSource value
                    if brknItem.supports("dataSource"):
                        f.write(", " + brknItem.dataSource + "\n")
                    else:
                        f.write("\n")
            except AttributeError:
                print "This MXD has unreadable dataframes {}".format(mxd.filePath)
            # Write the information for all .lyr's with broken data sources
        elif extension == ".lyr":
            fullPath = os.path.join(root, fileName)
            lyr = arcpy.mapping.Layer(fullPath)
            brknLYR = arcpy.mapping.ListBrokenDataSources(lyr)
            for brknItem in brknLYR:
                f.write("LYR, " + fullPath + ", " + brknItem.name)
                # Test to see if the data type is able to return a dataSource value
                if brknItem.supports("dataSource"):
                    f.write(", " + brknItem.dataSource + "\n")
                else:
                    f.write("\n")

f.close()

print "Script Completed"