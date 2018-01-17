#Import modules...
import arcpy, os, fnmatch, csv

#User input variables...
mxddirectory = arcpy.GetParameterAsText(0)
mxd_single = arcpy.GetParameterAsText(1)
outputcsvlocation = arcpy.GetParameterAsText(2)

#Create an empty list of ArcMap documents to process...
mxd_list=[]
#If a user defined a single mxd, add its path to the list...
if len(mxd_single) > 0:
  mxd_list.append(mxd_single)
#Otherwise walk through the input directory, adding paths for each .mxd file found to the list...

else:
  for dirpath in os.walk(mxddirectory): #os.walk returns \
    (dirpath, dirnames, filenames)
    for filename in dirpath[2]:
      if fnmatch.fnmatch(filename, "*.mxd"):
        mxd_list.append(os.path.join(dirpath[0], filename))

#Iterate the list of mxd paths and gather property values then write to csv file...
if len(mxd_list) > 0:
  #Create the csv file...
  outputcsv = open(outputcsvlocation,"wb")
  writer = csv.writer(outputcsv, dialect = 'excel')
  #Write a header row to the csv file...
  writer.writerow(["mxdpath", "layername", "layerdescription", "layersource"])
  #Iterate through the list of ArcMap Documents...
  for mxdpath in mxd_list:
    mxdname = os.path.split(mxdpath)[1]
    try:
      mxd = arcpy.mapping.MapDocument(mxdpath)
      #Iterate through the ArcMap Document layers...
      for layer in arcpy.mapping.ListLayers(mxd):
        layerattributes = [mxdpath, layer.longName,layer.description, layer.dataSource]
        #Write the attributes to the csv file...
        writer.writerow(layerattributes)
    except:
      arcpy.AddMessage("EXCEPTION: {0}".format(mxdpath))
    del mxd
  #close the csv file to save it...
  outputcsv.close()
#If no ArcMap Documents are in the list, then notify via an error message...
else:
  arcpy.AddError("No ArcMap Documents found. Please check your input variables.")