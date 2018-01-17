import arcpy, os

workspace = r'C:\Users\daniel.scott\Desktop\DataOwner\Dataowner@SRV-SQLHA02@DVC.sde'

arcpy.env.workspace = workspace

# NOTE: Rebuild indexes can accept a Python list of datasets.

# Get a list of all the datasets the user has access to.
# First, get all the stand alone tables, feature classes and rasters.
for dataset in arcpy.ListDatasets("", "Feature"):
    print dataset
    fclist = arcpy.ListFeatureClasses("*","",dataset)
    for fc in fclist:
        print "Indexes rebuilt for {0}".format(fc)

