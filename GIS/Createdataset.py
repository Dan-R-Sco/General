import arcpy, sys, os
arcpy.env.overwriteOutput = True
arcpy.env.workspace = arcpy.GetParameterAsText(0)
gdb = arcpy.env.workspace
datasettemp = arcpy.GetParameterAsText(1)
prjcode = arcpy.GetParameterAsText(2)
CRS = arcpy.GetParameterAsText(3)
fcs = arcpy.ListFeatureClasses("*","",datasettemp)
arcpy.CreateFeatureDataset_management(workspace, prjcode, CRS)

for fc in fcs:
    newname = fc.lstrip("Database Connections\admin_ndp@srv-sql03@egdtesting.sde\EGDB_Testing.ADMIN_NDP.TestATraining\EGDB_Testing.ADMIN_NDP.")
    arcpy.CopyFeatures_management(fc, gdb + "\\" + prjcode + "\\" + newname)